# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Synapse Session module."""

import json
import textwrap
import uuid

from sparkmagic.livyclientlib.exceptions import LivyClientTimeoutException, LivyUnexpectedStatusException
from sparkmagic.livyclientlib.livysession import LivySession
from sparkmagic.utils.constants import POSSIBLE_SESSION_STATUS, IDLE_SESSION_STATUS, FINAL_STATUS
from hdijupyterutils.ipythondisplay import IpythonDisplay

from . import consts
from . import utils
from .sessiontracker import SessionTracker
from .synapselivyreliablehttpclient import SynapseLivyReliableHttpClient
from . import telemetryutils


class SynapseSession(LivySession):
    """SynapseSession class wraps LivySession and add some Synapse specific session handling."""

    def __init__(self, subscription_id: str, resource_group: str, workspace: str, sparkpool: str,
                 properties: dict, timeout: int, ipython_display: IpythonDisplay):
        """Create the SynapseSession.

        :param subscription_id: subscription id
        :type subscription_id: str
        :param workspace: name of the Synapse workspace
        :type workspace: str
        :param sparkpool: name of the Synapse Spark pool
        :type sparkpool: str
        :param timeout: how long the session will timeout, in minutes
        :type timeout: int
        :param properties: a dictionary contains the settings of the session
        :type properties: dict
        :param ipython_display: ipython display
        :type ipython_display: IpythonDisplay
        """
        endpoint_url = utils.get_synapse_endpoint(workspace, sparkpool)
        self._http_client = SynapseLivyReliableHttpClient(endpoint_url)
        super(SynapseSession, self).__init__(self._http_client, properties, ipython_display)
        self.meta = {}
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace = workspace
        self.sparkpool = sparkpool
        self.session_tracker = None
        self.error = None
        self.timeout = timeout
        self.is_timeout = False
        self.show_dot_progress = False

    def start(self, timeout: int = 300):
        """Start the session."""
        # Override the LivySession.start to init SessionTracker and meta, and set the start timeout, 300s by default
        self._printed_resource_warning = False  # reset
        try:
            name = self.properties["name"]
            r = self._http_client.post_session(self.properties)
            env_desc = utils._get_env_desc(self.properties.get('environment'),
                                           self.properties.get('environmentVersion'))
            if env_desc is not None:
                utils.writeln("Warning: Only Conda dependencies in the environment will be used, and "
                              "Python dependency specified in environment Conda dependencies is not "
                              "supported in Synapse Spark pool. \nSynapse Spark pool now only supports fixed "
                              "Python version, you can print \"sys.version_info\" in your script to check "
                              "current Python version.")
                utils.writeln("Starting session '{}' under environment '{}', this may take several minutes "
                              .format(name, env_desc))
            else:
                utils.write("Starting session '{}', this may take several minutes ".format(name))
            self.id = r[u"id"]
            self.status = str(r[u"state"])

            # Wait for timeout seconds since the warm up of Synapse takes longer then normal Spark.
            self.show_dot_progress = True
            self.wait_for_idle(timeout)
            utils.writeln(" Succeeded!")
        except LivyClientTimeoutException:
            raise LivyClientTimeoutException(
                "Session {} did not start up in {} seconds. Consider use a longer --start-timeout or try later."
                .format(self.id, timeout))
        except LivyUnexpectedStatusException:
            # get detail session status for detail error msg
            livy_err_info = ""
            try:
                response = self._http_client.get_session(self.id, True)
                livy_err_info = str(response['errorInfo'])
                if "LIBRARY_MANAGEMENT_FAILED" in livy_err_info:
                    livy_err_info = ("Library management failed: The session could not be created as there was "
                                     "a problem installing the session specific libraries. "
                                     "Check or remove the provided environment configuration and try again.")
            finally:
                raise LivyUnexpectedStatusException(
                    "Start session failed at status {}. \n"
                    "Error info: {} \n"
                    "Please retry or go to Synapse portal {} for details."
                    .format(self.status, livy_err_info, self.get_synapse_app_url()))

        aml_workspace_details = telemetryutils.get_aml_workspace_details()
        self.meta = {
            "subscription_id": aml_workspace_details.get("subscription_id", None),
            "resource_group": aml_workspace_details.get("resource_group", None),
            "workspace_name": aml_workspace_details.get("workspace_name", None),
            "session_id": self.id,
            "application_id": self._app_id,
            "application_name": name,
            "application_url": self.get_synapse_app_url(),
            "spark_ui_url": self.get_spark_ui_url(),
            "driver_memory": self.properties["driverMemory"],
            "driver_cores": self.properties["driverCores"],
            "executor_memory": self.properties["executorMemory"],
            "executor_cores": self.properties["executorCores"],
            "num_executors": self.properties["numExecutors"],
            "environment_name": self.properties.get("environment"),
            "environment_version": self.properties.get("environmentVersion"),
            "spark_conf": self.properties.get("conf"),
            "start_timeout_seconds": self.properties["startTimeout"],
            "timeout_minutes": self.timeout,
        }
        self.session_tracker = SessionTracker(self)
        self.session_tracker.session_create_end()

    def get_synapse_app_url(self):
        """Get the url of the Synapse Spark application."""
        if self.subscription_id is None or self.resource_group is None:
            return "unknown"
        return consts.SYNAPSE_UI_URL_TEMPLATE.format(self._app_id, self.subscription_id, self.resource_group,
                                                     self.workspace, self.id, self.sparkpool)

    def get_spark_ui_url(self):
        """Get the url of the Spark UI."""
        return consts.SPARK_UI_URL_TEMPLATE.format(self.workspace, self.sparkpool, self.id, self._app_id)

    def show_meta(self):
        """Show session meta data in notebook."""
        self.meta["application_state"] = self.status
        utils.writeln(json.dumps(self.meta, indent=4, sort_keys=True))

    def delete(self):
        """Delete the session."""
        self.session_tracker.session_delete_end()
        try:
            super(SynapseSession, self).delete()
        except Exception:
            raise

    def execute(self, code: str, kind):
        """Execute some Spark code.

        :param code: the Spark code to be executed
        :type code: str
        :param kind: the Spark language of the code, supported language include: spark(Scala), pyspark, csharp and sql
        :type kind: str
        """
        assert self.can_submit()
        assert code is not None
        assert kind is not None
        self.show_dot_progress = False
        try:
            self.wait_for_idle()
        except LivyUnexpectedStatusException:
            raise LivyUnexpectedStatusException(
                "Session failed at status {}. "
                "Please run stop and start a new session or go to Synapse portal {} for details.".format(
                    self.status,
                    self.get_synapse_app_url()))
        code = textwrap.dedent(code)
        response = self.http_client.post_statement(self.id, {"code": code, "kind": kind})
        statement_id = response[u'id']
        # here is the trick, we are not able to get the real cell id from frontend, just create a new guid for it
        # but since there will be only one running cell in notebook, frontend can match this new guid to it
        self.session_tracker.statement_execution_start(str(uuid.uuid4()), statement_id)

    def refresh_status_and_info(self):
        """Refresh the latest status of the session."""
        # Override the one from LivySession to get appId and print dots for long session start
        if self.show_dot_progress:
            utils.write(".")
        response = self._refresh_status()
        log_array = response[u'log']
        if log_array:
            self.session_info = "\n".join(log_array)

    def _refresh_status(self):
        response = self._http_client.get_session(self.id)
        status = response[u"state"]
        if status in POSSIBLE_SESSION_STATUS:
            self.status = status
            if self._app_id is None and response[u"appId"]:
                self._app_id = response[u"appId"]
        else:
            raise LivyUnexpectedStatusException("Status '{}' not supported by session.".format(status))
        self._reset_timeout_when_needed()
        return response

    def mark_timeout(self):
        """Mark the session as a timeout session to let it timeout."""
        self.status = consts.SESSION_STATUS_TIMEOUT
        self.is_timeout = True

    def can_submit(self):
        """Check if we can submit a job within this session."""
        is_final_status = self.status in FINAL_STATUS
        return not is_final_status and not self.is_timeout

    def _reset_timeout_when_needed(self):
        if IDLE_SESSION_STATUS == self.status and not self.is_timeout:
            self._http_client.reset_session_timeout(self.id)

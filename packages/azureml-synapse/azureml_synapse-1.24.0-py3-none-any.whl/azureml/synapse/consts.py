# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Constants definition."""

from sparkmagic.utils import constants

CREDENTIALS_resource = "https://dev.azuresynapse.net"

SESSION_STATUS_STARTING = "starting"
SESSION_STATUS_STARTED = "started"
SESSION_STATUS_BUSY = "busy"
SESSION_STATUS_IDLE = "idle"
SESSION_STATUS_DEAD = "dead"
SESSION_STATUS_TIMEOUT = "timeout"
SESSION_STATUS_STOPPED = "stopped"


SESSION_KIND_PYSPARK = constants.SESSION_KIND_PYSPARK
SESSION_KIND_SPARK = constants.SESSION_KIND_SPARK
SESSION_KIND_CSHARP = "csharp"
SESSION_KIND_SQL = "sql"
SESSION_KINDS_SUPPORTED = [SESSION_KIND_SPARK, SESSION_KIND_PYSPARK, SESSION_KIND_CSHARP, SESSION_KIND_SQL]

LIVY_ENDPOINT_TEMPLATE = "https://{}.dev.azuresynapse.net/livyApi/versions/2019-11-01-preview/sparkPools/{}"
SYNAPSE_UI_URL_TEMPLATE = "https://web.azuresynapse.net/monitoring/sparkapplication/{}?" \
                          "workspace=/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Synapse/workspaces/{}" \
                          "&livyId={}&sparkPoolName={}"
SPARK_UI_URL_TEMPLATE = "https://web.azuresynapse.net/sparkui/dev.azuresynapse.net/" \
                        "workspaces/{}/sparkpools/{}/livyid/{}/history/{}/1/"

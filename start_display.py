from collections import namedtuple

from hifi_appliance.display import Display
from hifi_appliance.config import DAEMON_GROUP
from hifi_appliance.config import DAEMON_USER
from hifi_appliance.config import DEBUG
from hifi_appliance.config import LOG_FILE_DISPLAY
from hifi_appliance.config import PID_FILE_DISPLAY


daemon_config = namedtuple(
    'DaemonConfig',
    ['user', 'group', 'initgroups', 'pid_file', 'log_file']
)
daemon_config.user = DAEMON_USER
daemon_config.group = DAEMON_GROUP
daemon_config.initgroups = False
daemon_config.pid_file = PID_FILE_DISPLAY
daemon_config.log_file = LOG_FILE_DISPLAY


display = Display(daemon_config, debug=DEBUG)

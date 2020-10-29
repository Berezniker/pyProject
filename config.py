from collections import namedtuple
from enum import Enum
import platform
import os


class OSType(Enum):
    Windows = 0
    Linux = 1
    Mac = 2


def get_os_type() -> OSType:
    """
    returns the operating system type: OneOf[Windows, Linux, Mac]

    :return: OSType
    """
    os_name = platform.system()
    if os_name == "Windows":
        return OSType.Windows
    elif os_name == "Linux":
        return OSType.Linux
    elif os_name == "Darwin":
        return OSType.Mac


# CHANGE THIS!
PROJECT_PATH = "C:\\Users\\Alexey\\Desktop\\study\\Diplom\\pyProject"

DATA_PATH = os.path.join(PROJECT_PATH, "data")

CODE_PATh = os.path.join(PROJECT_PATH, "src")

APP_NAME = "MMouse"

APP_PATH = os.path.join(PROJECT_PATH, APP_NAME)

USER_DATABASE_NAME = "userDB"

USER_DATABASE_PATH = os.path.join(DATA_PATH, USER_DATABASE_NAME)

OS_TYPE = get_os_type()

if OS_TYPE == OSType.Mac:
    ICON_APP_NAME = "mickey_mouse.icns"
    ICON_NOTIFICATION_NAME = "alarm.icns"
else:
    ICON_APP_NAME = "mickey_mouse.ico"
    ICON_NOTIFICATION_NAME = "alarm.ico"

ICON_APP_PATH = os.path.join(DATA_PATH, ICON_APP_NAME)

ICON_NOTIFICATION_PATH = os.path.join(DATA_PATH, ICON_NOTIFICATION_NAME)

TTIME_VALUE: float = 3.0

MIN_N_ACTION: int = 5

DURATION_NOTIFICATION: int = 5

RawData = namedtuple(
    typename="RawData",
    field_names="timestamp, button, state, x, y"
)

Data = namedtuple(
    typename="Data",
    field_names="timestamp, x, y"
)
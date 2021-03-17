from typing import List, Dict, Union
from collections import namedtuple
from enum import Enum
import platform
import logging
import os


PROJECT_PATH: str = os.getcwd()

# --------------------------------------------------

DATA_PATH: str = os.path.join(PROJECT_PATH, "data")

CODE_PATH: str = os.path.join(PROJECT_PATH, "src")

LOG_PATH: str = os.path.join(DATA_PATH, "log")

TEST_MODE_PATH: str = os.path.join(DATA_PATH, "test_mode")

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


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


OS_TYPE: OSType = get_os_type()

# --- main.py

DURATION_NOTIFICATION: int = 5

LOG_LEVEL_DEBUG: str = "debug"
LOG_LEVEL_INFO: str = "info"
LOG_LEVEL_WARNING: str = "warning"
LOG_LEVEL_ERROR: str = "error"
LOG_LEVEL_CRITICAL: str = "critical"

LOGGING_LEVEL: List[str] = [
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_INFO,
    LOG_LEVEL_WARNING,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_CRITICAL
]

ARGS_TO_LEVEL: Dict[str, int] = {
    LOG_LEVEL_DEBUG: logging.DEBUG,
    LOG_LEVEL_INFO: logging.INFO,
    LOG_LEVEL_WARNING: logging.WARNING,
    LOG_LEVEL_ERROR: logging.ERROR,
    LOG_LEVEL_CRITICAL: logging.CRITICAL
}

# --------------------------------------------------

# --- compile.py

APP_NAME: str = "MMouse"

APP_PATH: str = os.path.join(PROJECT_PATH, APP_NAME)

if OS_TYPE == OSType.Mac:
    ICON_APP_NAME: str = "mickey_mouse.icns"
else:
    ICON_APP_NAME: str = "mickey_mouse.ico"

ICON_APP_PATH: str = os.path.join(DATA_PATH, ICON_APP_NAME)

# --------------------------------------------------

# --- src.notification.py

if OS_TYPE == OSType.Mac:
    ICON_NOTIFICATION_NAME: str = "alarm.icns"
else:
    ICON_NOTIFICATION_NAME: str = "alarm.ico"

ICON_NOTIFICATION_PATH: str = os.path.join(DATA_PATH, ICON_NOTIFICATION_NAME)

# --------------------------------------------------

# --- src.logger.py

TTIME_VALUE: float = 3.0

# --------------------------------------------------

# --- src.*.database.py

USER_DATABASE_NAME: str = "userDB"

USER_DATABASE_PATH: str = os.path.join(DATA_PATH, USER_DATABASE_NAME)

USER_TABLE_NAME: str = "login"

DATA_TABLE_NAME: str = "data"

# --------------------------------------------------

# --- src.pipeline.preprocessing.py

RawData = namedtuple(
    typename="RawData",
    field_names="timestamp, button, state, x, y"
)

MIN_N_ACTION: int = 5

# --------------------------------------------------

# --- src.pipeline.model.py

TRUST_MODEL_PARAMS: Dict[str, float] = {
    "A": 0.00,
    "B": 0.25,
    "C": 1.00,
    "D": 1.00,
    "lockout": 90.0
}

ONE_CLASS_SVM_PARAMS: Dict[str, Union[str, float]] = {
    "kernel": "rbf",
    "gamma": "scale",
    "nu": 0.05
}

MIN_TRAIN_SIZE: int = 100000

# --------------------------------------------------

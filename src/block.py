import config
import ctypes
import os


def block() -> None:
    """
    Block the system

    :return: None
    """
    if config.OS_TYPE == config.OSType.Windows:
        ctypes.windll.user32.LockWorkStation()
    elif config.OS_TYPE == config.OSType.Linux:
        command = "loginctl lock-session"
        os.system(command)
    elif config.OS_TYPE == config.OSType.Mac:
        command = r"/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend"
        os.system(command)
    return


if __name__ == '__main__':
    print("Run!")
    block()
    print("End of run.")

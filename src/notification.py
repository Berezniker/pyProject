import win10toast
import config
import time
import os


def notification(title: str,
                 message: str,
                 duration: float = 5.0) -> None:
    """
    Displays notifications in the taskbar

    :param title: the headline of the message
    :param message: message text
    :param duration: duration of notification
    :return: None
    """
    if config.OS_TYPE == config.OSType.Windows:
        win10toast.ToastNotifier().show_toast(
            title=title,
            msg=message,
            icon_path=config.ICON_NOTIFICATION_PATH,
            duration=duration
        )
    elif config.OS_TYPE == config.OSType.Mac:
        # http://osxh.ru/terminal/command/osascript
        command = f'''osascript -s h -e 'display notification "{message}" with title "{title}"'''
        os.system(command)
        time.sleep(duration)
    elif config.OS_TYPE == config.OSType.Linux:
        # http://manpages.ubuntu.com/manpages/bionic/man1/notify-send.1.html
        command = f'''
            notify-send
                --urgency=critical
                --expire-time={duration}
                --icon={config.ICON_NOTIFICATION_PATH}
                "{title}"
                "{message}"
        '''
        command = " ".join(command.split())  # must be in one line
        os.system(command)
    return


if __name__ == '__main__':
    print("Run!")
    notification(
        title="title",
        message="message",
        duration=5
    )
    print("End.")

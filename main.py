from src.authorization.authorization import authorization
from src.notification import notification
from src.logger import data_capture_loop
from src.block import block
import config


if __name__ == '__main__':
    try:
        duration = config.DURATION_NOTIFICATION
        while True:
            authorization()
            data_capture_loop()
            notification(title="Attention!",
                         message=f"The system will be locked after {duration} seconds ...",
                         duration=duration)
            block()
    except (KeyboardInterrupt, EOFError):
        # Ctrl-C, Ctrl-Z, Ctrl-D signal handler
        pass

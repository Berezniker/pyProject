from src.authorization.authorization import authorization
from src.notification import notification
from src.logger import data_capture_loop
from src.block import block
from config import DURATION_NOTIFICATION


if __name__ == '__main__':
    try:
        while True:
            user_id = authorization()
            data_capture_loop(user_id)
            notification(title="Attention!",
                         message=f"The system will be locked "\
                                 f"after {DURATION_NOTIFICATION} seconds ...",
                         duration=DURATION_NOTIFICATION)
            block()
    except (KeyboardInterrupt, EOFError):
        # Ctrl-C, Ctrl-Z, Ctrl-D signal handler
        pass

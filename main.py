from src.authorization.authorization import authorization
from src.notification import notification
from src.logger import data_capture_loop
from src.block import system_lock
from config import DURATION_NOTIFICATION


if __name__ == '__main__':
    try:
        while True:
            # -------------------------
            # 1.
            user_id = authorization()
            if user_id == -1:
                # if close LogIn Form
                break
            # 2.
            data_capture_loop(user_id)
            # 3.
            notification(
                title="Attention!",
                message=f"The system will be locked "
                        f"after {DURATION_NOTIFICATION} seconds ...",
                duration=DURATION_NOTIFICATION
            )
            # 4.
            system_lock()
            # -------------------------
    except (KeyboardInterrupt, EOFError):
        # Ctrl-C, Ctrl-Z, Ctrl-D signal handler
        pass

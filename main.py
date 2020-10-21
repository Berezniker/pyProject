from src.authorization.authorization import authorization
from src.notification import notification
from src.logger import data_capture_loop
from src.block import block


if __name__ == '__main__':
    while True:
        authorization()
        data_capture_loop()
        notification(title="Attention!",
                     message="The system will be locked after 5 seconds ...",
                     duration=5)
        block()

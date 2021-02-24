from src.authorization.authorization import authorization, one_shot_login
from src.notification import notification
from src.logger import data_capture_loop
from src.block import system_lock
from config import DURATION_NOTIFICATION
import argparse
import logging


# link:
# https://docs.python.org/3/library/argparse.html


def add_arguments(argparser) -> None:
    """
    Parse command line arguments

    :return: None
    """
    argparser.add_argument("-l", "--login", dest="login", type=str)
    argparser.add_argument("-p", "--password", dest="password", type=str)
    return


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Mouse continuous authentication")
    add_arguments(argparser)
    args = argparser.parse_args()
    try:
        while True:
            # 1
            logging.info("Start authorization")
            if args.login and args.password:
                logging.info("Get login & password from arguments")
                user_id = one_shot_login(
                    login=args.login,
                    password=args.password
                )
            else:
                user_id = authorization()
            if user_id == -1:
                logging.info("Close LogIn Form")
                break
            # 2.
            logging.info("Start data capture")
            data_capture_loop(user_id)
            # 3.
            logging.info("Send notification")
            notification(
                title="Attention!",
                message=f"The system will be locked "
                        f"after {DURATION_NOTIFICATION} seconds ...",
                duration=DURATION_NOTIFICATION
            )
            # 4.
            logging.info("Block system")
            system_lock()
    except (KeyboardInterrupt, EOFError):
        # Ctrl-C, Ctrl-Z, Ctrl-D signal handler
        logging.info("Signal received")
        pass

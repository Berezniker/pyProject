from src.authorization.authorization import authorization, one_shot_login
from src.notification import notification
from src.logger import data_capture_loop
from src.block import system_lock
from config import (
    DURATION_NOTIFICATION, MIN_N_ACTION, MIN_TRAIN_SIZE,
    ONE_CLASS_SVM_PARAMS, TRUST_MODEL_PARAMS, TTIME_VALUE
)
import argparse
import logging


# link:
# https://docs.python.org/3/library/argparse.html


def add_arguments(argparser) -> None:
    """
    Parse command line arguments

    param argparser: argparse.ArgumentParser
    :return: None
    """
    # LogIn Params:
    argparser.add_argument("-l", "--login", dest="login", type=str)
    argparser.add_argument("-p", "--password", dest="password", type=str)

    argparser.add_argument("--ttime-value", dest="ttime_value", type=str, default=TTIME_VALUE)
    argparser.add_argument("--min-n-action", dest="min_n_action", type=str, default=MIN_N_ACTION)
    argparser.add_argument("--min-train-size", dest="min_train_size", type=str, default=MIN_TRAIN_SIZE)
    argparser.add_argument("--duration-notification", dest="duration_notification", type=str,
                           default=DURATION_NOTIFICATION)

    # Trust Model Params:
    argparser.add_argument("-A", "--trust-model-a", dest="trust_model_a", type=str,
                           default=TRUST_MODEL_PARAMS["A"])
    argparser.add_argument("-B", "--trust-model-b", dest="trust_model_b", type=str,
                           default=TRUST_MODEL_PARAMS["B"])
    argparser.add_argument("-C", "--trust-model-c", dest="trust_model_c", type=str,
                           default=TRUST_MODEL_PARAMS["C"])
    argparser.add_argument("-D", "--trust-model-d", dest="trust_model_d", type=str,
                           default=TRUST_MODEL_PARAMS["D"])
    argparser.add_argument("--trust-model-lockout", dest="trust_model_lockout", type=str,
                           default=TRUST_MODEL_PARAMS["lockout"])

    # OneClassSVM Params:
    argparser.add_argument("--one-class-svm-kernel", dest="one_class_svm_kernel", type=str,
                           default=ONE_CLASS_SVM_PARAMS["kernel"])
    argparser.add_argument("--one-class-svm-gamma", dest="one_class_svm_gamma", type=str,
                           default=ONE_CLASS_SVM_PARAMS["gamma"])
    argparser.add_argument("--one-class-svm-nu", dest="one_class_svm_nu", type=str,
                           default=ONE_CLASS_SVM_PARAMS["nu"])
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
            data_capture_loop(
                user_id=user_id,
                args=args
            )
            # 3.
            logging.info("Send notification")
            notification(
                title="Attention!",
                message=f"The system will be locked "
                        f"after {args.duration_notification} seconds ...",
                duration=args.duration_notification
            )
            # 4.
            logging.info("Block system")
            system_lock()
    except (KeyboardInterrupt, EOFError):
        # Ctrl-C, Ctrl-Z, Ctrl-D signal handler
        logging.info("Signal received")
        pass

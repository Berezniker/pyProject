from src.authorization.authorization import authorization, one_shot_login
from src.test_mode.run import run_test_mode
from src.notification import notification
from src.logger import data_capture_loop
from src.block import system_lock
from config import (
    DURATION_NOTIFICATION, MIN_N_ACTION, MIN_TRAIN_SIZE,
    ONE_CLASS_SVM_PARAMS, TRUST_MODEL_PARAMS, TTIME_VALUE,
    ARGS_TO_LEVEL, LOGGING_LEVEL
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

    # Common Params:
    argparser.add_argument("--ttime-value", dest="ttime_value", type=float, default=TTIME_VALUE)
    argparser.add_argument("--min-n-action", dest="min_n_action", type=int, default=MIN_N_ACTION)
    argparser.add_argument("--min-train-size", dest="min_train_size", type=int, default=MIN_TRAIN_SIZE)
    argparser.add_argument("--duration-notification", dest="duration_notification", type=int,
                           default=DURATION_NOTIFICATION)
    argparser.add_argument("--log-level", dest="log_level", type=str, default="info",
                           choices=LOGGING_LEVEL, help="Python built-in logging level")

    # Trust Model Params:
    argparser.add_argument("-A", "--trust-model-a", dest="trust_model_a", type=float,
                           default=TRUST_MODEL_PARAMS["A"])
    argparser.add_argument("-B", "--trust-model-b", dest="trust_model_b", type=float,
                           default=TRUST_MODEL_PARAMS["B"])
    argparser.add_argument("-C", "--trust-model-c", dest="trust_model_c", type=float,
                           default=TRUST_MODEL_PARAMS["C"])
    argparser.add_argument("-D", "--trust-model-d", dest="trust_model_d", type=float,
                           default=TRUST_MODEL_PARAMS["D"])
    argparser.add_argument("--trust-model-lockout", dest="trust_model_lockout", type=float,
                           default=TRUST_MODEL_PARAMS["lockout"])

    # OneClassSVM Params:
    argparser.add_argument("--one-class-svm-kernel", dest="one_class_svm_kernel", type=str,
                           default=ONE_CLASS_SVM_PARAMS["kernel"])
    argparser.add_argument("--one-class-svm-gamma", dest="one_class_svm_gamma", type=str,
                           default=ONE_CLASS_SVM_PARAMS["gamma"])
    argparser.add_argument("--one-class-svm-nu", dest="one_class_svm_nu", type=float,
                           default=ONE_CLASS_SVM_PARAMS["nu"])

    # Test Mode Param
    argparser.add_argument("--test-mode", dest="test_mode", action="store_true",
                           help="If Active, Run Program in Test Mode")
    argparser.add_argument("--real-user-id", dest="real_user_id", type=str)
    argparser.add_argument("--illegal-user-id", dest="illegal_user_id", type=str)
    argparser.add_argument("--illegal-duration", dest="illegal_duration", type=int, default=120,
                           help="Duration of implementation (in seconds)")
    return


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Mouse continuous authentication")
    add_arguments(argparser)
    args = argparser.parse_args()
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=ARGS_TO_LEVEL[args.log_level]
    )

    # ----- Test Mode -----
    if args.test_mode:
        run_test_mode(args)
        logging.info("Test Mode Failed")
        notification(
            title="Attention!",
            message=f"Test Mode Failed!",
            duration=args.duration_notification
        )
        exit(0)
    # ---------------------

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

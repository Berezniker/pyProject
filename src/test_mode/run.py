from src.pipeline.model import authentication
from config import TEST_MODE_PATH
import numpy as np
import time
import csv


start_time_implementation: float = time.time()


def get_user_id(args) -> int:
    """
    Select user and return their ID

    :param args: Command line arguments
    :return: User ID
    """
    if (time.time() - start_time_implementation) < args.illegal_duration:
        return args.real_user_id
    else:
        return args.illegal_user_id


def get_feature(user_id: int) -> np.ndarray:
    """
    Get feature-vector

    :param user_id: User ID
    :yield: feature
    """
    with open(f"{TEST_MODE_PATH}/{user_id}_test_data.csv", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            yield np.array(row)


def run_test_mode(args) -> None:
    """
    Run Test Mode

    :param args: Command line arguments
    :return: None
    """
    get_real_user_feature = get_feature(args.real_user_id)
    get_illegal_user_feature = get_feature(args.illegal_user_id)
    user_id_to_getter = {
        args.real_user_id: get_real_user_feature,
        args.illegal_user_id: get_illegal_user_feature
    }
    while True:
        user_id = get_user_id(args=args)
        feature = next(user_id_to_getter[user_id])
        if not authentication(
            user_id=args.real_user_id,
            feature=feature,
            args=args
        ):
            break  # block
    return


if __name__ == "__main__":
    pass

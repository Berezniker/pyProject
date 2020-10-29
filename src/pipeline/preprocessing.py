from config import MIN_N_ACTION, RawData
from typing import List
import numpy as np


def _quartile(data: np.ndarray, col: int) -> np.ndarray:
    """
    Replace the values in <data[col]> outside the IQR
    with the upper and lower boundaries, respectively.

    :param data: data
    :param col: column index
    :return: transformed data
    """
    q1 = np.percentile(data[:, col], q=25)  # lower (first) quartile
    q3 = np.percentile(data[:, col], q=75)  # upper (third) quartile
    iqr = q3 - q1  # InterQuartileRange
    lower_fence = (q1 - 1.5 * iqr)
    upper_fence = (q3 + 1.5 * iqr)
    data[data[:, col] < lower_fence, col] = lower_fence
    data[data[:, col] > upper_fence, col] = upper_fence
    return data


def preprocessing(raw_data: List[RawData]) -> np.ndarray:
    """
    Full preprocessing of raw data

    :param raw_data: raw data
    :return: preprocessed data
    """
    data = list()
    if len(raw_data) < MIN_N_ACTION:
        return np.array([])

    # for each observation...
    for i in range(len(raw_data) - 1):  # skip last observation
        timestamp, _, _, x, y = raw_data[i]
        # Drop Duplicates
        if raw_data[i - 1] == raw_data[i]:
            continue
        # Fix Time Duplicate
        if raw_data[i - 1].timestamp == timestamp:
            timestamp = (raw_data[i - 1].timestamp +
                         raw_data[i + 1].timestamp) / 2.0
        # Fix Negative Coordinates
        x = max(x, 0)
        y = max(y, 0)

        data.append((timestamp, x, y))

    data = np.array(data)      # `list` to `np.array`
    data = _quartile(data, 1)  # for `x`
    data = _quartile(data, 2)  # for `y`

    return data


if __name__ == "__main__":
    print("Run!")
    # preprocessing(...)
    print("End of run.")

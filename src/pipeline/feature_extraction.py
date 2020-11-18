import numpy as np


def direction_bin(data: np.ndarray, n_bin: int = 8) -> np.ndarray:
    """
    ...

    :param data: (x, y)-coordinates
    :param n_bin: number of bins
    :return: ...
    """
    grad_x, grad_y = np.gradient(data[:, 1]), np.gradient(data[:, 2])
    direction = np.rad2deg(np.arctan2(grad_y, grad_x)) + 180
    direction = (direction % n_bin).astype(np.uint8)
    return np.argmax(np.bincount(direction))


def get_det(data: np.ndarray) -> np.ndarray:
    """
    ...

    :param data: ...
    :return: ...
    """
    Pn_Po = np.array([data[-1, 1] - data[0, 1], data[-1, 2] - data[0, 2]])
    x0, y0 = data[0, 1], data[0, 2]
    det = np.array([np.linalg.det([Pn_Po, [x - x0, y - y0]])
                    for x, y in zip(data[1:, 1], data[1:, 2])])
    return det


def get_bin(dist: int, threshold: int = 1000) -> int:
    """
    ...

    :param dist: ...
    :param threshold: threshold
    :return: bin
    """
    if dist <= threshold:
        return dist // (threshold // 5)
    elif dist <= 2 * threshold:
        return 5 + (dist - threshold) // (threshold // 10)
    elif dist <= 3 * threshold:
        return 15 + (dist - 2 * threshold) // (threshold // 4)
    else:
        return 19


def extractor(data: np.ndarray) -> np.ndarray:
    """
    extraction_function:
        direction_bin, actual_distance, actual_distance_bin,
        curve_length, curve_length_bin, length_ratio, actual_speed, curve_speed,
        curve_acceleration, mean_movement_offset, mean_movement_error,
        mean_movement_variability, mean_curvature, mean_curvature_change_rate,
        mean_curvature_velocity, mean_curvature_velocity_change_rate, mean_angular_velocity

    :param: data - np.array - shape=(N, 3)=(N, `(timestamp, x, y)`)
    :return: feature - np.array = shape=(1, 16)
    """
    dt = np.diff(data[:, 0])
    # dt[dt == 0] = 1e-3  # no duplicate timestamps
    dx = np.diff(data[:, 1])
    dy = np.diff(data[:, 2])
    dttm = data[-1, 0] - data[0, 0]  # < config.TTIME_VALUE

    # 1.
    actual_distance = ((data[0, 1] - data[-1, 1]) ** 2 +
                       (data[0, 2] - data[-1, 2]) ** 2) ** 0.5

    # 2.
    actual_distance_bin = get_bin(actual_distance, threshold=1000)

    # 3.
    curve_length = np.nansum(np.hypot(dx, dy))

    # 4.
    curve_length_bin = get_bin(curve_length, threshold=1000)

    # 5.
    length_ratio = 0.0 if actual_distance == 0.0 else \
        curve_length / actual_distance

    # 6.
    actual_speed = 0.0 if dttm == 0.0 else \
        actual_distance / dttm

    # 7.
    curve_speed = np.mean(np.hypot(dx, dy) / dt)

    # 8.
    curve_acceleration = 0.0 if dttm == 0.0 else \
        curve_speed / dttm

    # 9.
    Pn_P0 = np.array([data[-1, 1] - data[0, 1], data[-1, 2] - data[0, 2]])
    norm = np.linalg.norm(Pn_P0)
    det = get_det(data)
    mean_movement_offset = 0.0 if norm == 0.0 else \
        np.mean(det / norm)

    # 10.
    mean_movement_error = 0.0 if norm == 0.0 else \
        np.mean(np.abs(det / norm))

    # 11.
    mean_movement_variability = \
        np.mean(np.square(data[1:-1, 2] - mean_movement_offset)) ** 0.5

    # 12.
    xy = np.hypot(data[:, 1], data[:, 2])
    mask = (xy != 0)
    mean_curvature = 0.0 if np.all(~mask) else \
        np.mean(np.arctan2(data[:, 2], data[:, 1])[mask] / xy[mask])

    # 13.
    xy = np.hypot(data[-1, 1] - data[:-1, 1],
                  data[-1, 2] - data[:-1, 2])
    mask = (xy != 0)
    mean_curvature_change_rate = 0.0 if np.all(~mask) else \
        np.mean(np.arctan2(data[:-1, 2], data[:-1, 1])[mask] / xy[mask])

    # 14.
    mean_curvature_velocity = 0.0 if dttm == 0.0 else \
        mean_curvature / dttm

    # 15.
    mean_curvature_velocity_change_rate = 0.0 if dttm == 0.0 else \
        mean_curvature_velocity / dttm

    # 16.
    a = np.array([data[:-2, 1] - data[1:-1, 1],
                  data[:-2, 2] - data[1:-1, 2]])
    b = np.array([data[2:, 1] - data[1:-1, 1],
                  data[2:, 2] - data[1:-1, 2]])
    norm = np.linalg.norm(a, axis=0) * np.linalg.norm(b, axis=0)
    mask = (norm != 0)
    if np.all(~mask):
        mean_angular_velocity = 0.0
    else:
        x = np.minimum(1, np.maximum(-1, np.sum(a * b, axis=0)[mask] / norm[mask]))
        angle = np.arccos(x)
        dt = (data[2:, 0] - data[:-2, 0])[mask]
        mean_angular_velocity = np.mean(angle / dt)

    feature = np.array([
        direction_bin(data, n_bin=8),
        actual_distance,
        actual_distance_bin,
        curve_length,
        curve_length_bin,
        length_ratio,
        actual_speed,
        curve_speed,
        curve_acceleration,
        mean_movement_offset,
        mean_movement_error,
        mean_movement_variability,
        mean_curvature,
        mean_curvature_change_rate,
        mean_curvature_velocity,
        mean_curvature_velocity_change_rate,
        mean_angular_velocity
    ])
    # len(features) = 17

    return feature


if __name__ == "__main__":
    pass

import numpy as np


# TODO проверить функцию
def get_grad(val: np.ndarray) -> np.ndarray:
    return np.array([val[1], *(val[2:] - val[:-2]), -val[-2]])


def direction_bin(data: np.ndarray, n_bin: int = 8) -> np.ndarray:
    grad_x, grad_y = get_grad(data[:, 1]), get_grad(data[:, 2])
    direction = np.rad2deg(np.arctan2(grad_y, grad_x)) + 180
    direction = (direction % n_bin).astype(np.uint8)
    return np.argmax(np.bincount(direction))


def get_det(data: np.ndarray) -> np.ndarray:
    Pn_Po = np.array([data[-1, 1] - data[0, 1], data[-1, 2] - data[0, 2]])
    x0, y0 = data[0, 1], data[0, 2]
    det = np.array([np.linalg.det([Pn_Po, [x - x0, y - y0]])
                    for x, y in zip( data[1:, 1], data[1:, 2])])
    return det


def get_bin(dist: int, threshold: int = 1000) -> int:
    if dist <= threshold:
        return dist // (threshold // 5)
    elif dist <= 2 * threshold:
        return 5 + (dist - threshold) // (threshold // 10)
    elif dist <= 3 * threshold:
        return 15 + (dist - 2 * threshold) // (threshold // 4)
    else:
        return 19


def extractor(data: np.ndarray) -> None:
    """
    extraction_function:
        direction_bin, actual_distance, actual_distance_bin,
        curve_length, curve_length_bin, length_ratio, actual_speed, curve_speed,
        curve_acceleration, mean_movement_offset, mean_movement_error,
        mean_movement_variability, mean_curvature, mean_curvature_change_rate,
        mean_curvature_velocity, mean_curvature_velocity_change_rate, mean_angular_velocity

    :param: data - np.array - shape=(N, 3)=(N, `(timestamp, x, y)`)
    :return: None
    """
    dt = data[:, 0].diff()
    dt[dt == 0] = 1e-3  # не должно быть нулей: проверить
    dx = data[:, 1].diff()
    dy = data[:, 2].diff()
    dttm = data[-1, 0] - data[0, 0]

    # ------------------------------------------------------------ #
    actual_distance = ((data[0, 1] - data[-1, 1]) ** 2 +
                       (data[0, 2] - data[-1, 2]) ** 2) ** 0.5
    # ------------------------------------------------------------ #
    actual_distance_bin = get_bin(actual_distance, threshold=1000)
    # ------------------------------------------------------------ #
    curve_length = np.nansum(np.hypot(dx, dy))
    # ------------------------------------------------------------ #
    curve_length_bin = get_bin(curve_length, threshold=1000)
    # ------------------------------------------------------------ #
    length_ratio = 0.0 if actual_distance == 0.0 else \
        curve_length / actual_distance
    # ------------------------------------------------------------ #
    actual_speed = 0.0 if dttm == 0.0 else \
        actual_distance / dttm
    # ------------------------------------------------------------ #
    curve_speed = np.mean(np.hypot(dx, dy) / dt)
    # ------------------------------------------------------------ #
    curve_acceleration = 0.0 if dttm == 0.0 else \
        curve_speed / dttm
    # ------------------------------------------------------------ #
    Pn_P0 = np.array([data[-1, 1] - data[0, 1], data[-1, 2]])
    norm = np.linalg.norm(Pn_P0)
    det = get_det(data)

    mean_movement_offset = 0.0 if norm == 0.0 else \
        np.mean(det / norm)
    # ------------------------------------------------------------ #
    mean_movement_error = 0.0 if norm == 0.0 else \
        np.mean(np.abs(det / norm))
    # ------------------------------------------------------------ #
    mean_movement_variability = \
        np.mean((data[1:-1, 2] - mean_movement_offset) ** 2) ** 0.5
    # ------------------------------------------------------------ #
    xy = np.hypot(data[:, 1], data[:, 2])
    mask = (xy != 0)
    mean_curvature = 0.0 if np.all(~mask) else \
        np.mean(np.arctan2(data[:, 2], data[:, 1])[mask] / xy[mask])
    # ------------------------------------------------------------ #
    xy = ((data[-1, 1] - data[:-1, 1]) ** 2 +
          (data[-1, 2] - data[:-1, 2]) ** 2) ** 0.5
    mask = (xy != 0)
    mean_curvature_change_rate = 0.0 if np.all(~mask) else \
        np.mean(np.arctan2(data[:-1, 2], data[:-1, 1])[mask] / xy[mask])
    # ------------------------------------------------------------ #
    mean_curvature_velocity = 0.0 if dttm == 0.0 else \
        mean_curvature / dttm
    # ------------------------------------------------------------ #
    mean_curvature_velocity_change_rate = 0.0 if dttm == 0.0 else \
        mean_curvature_velocity / dttm
    # ------------------------------------------------------------ #
    mean_angular_velocity = ...
    # ------------------------------------------------------------ #
    feature = [
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
    ]

    # TODO: feature to database
    return


if __name__ == "__main__":
    print("Run!")
    # extractor(...)
    print("End of run.")

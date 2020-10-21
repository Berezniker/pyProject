from src.utils.cashe import cached
import pandas as pd
import numpy as np


# ARTICLE:
#
# Mondal S., Bours P. A study on continuous authentication using a combination of
# keystroke and mouse biometrics //Neurocomputing. – 2017. – Ò. 230. – Ñ. 1-22.


# feature extraction function template:
#
# def feature_name(db: pd.DataFrame) -> float:
#     """
#     extract features <features_name> from the database <db>
#     :param db: database segment
#     :return: feature value
#     """

def get_bin(dist: int, threshold: int = 1000) -> int:
    if dist <= threshold:
        return dist // (threshold // 5)
    elif dist <= 2 * threshold:
        return 5 + (dist - threshold) // (threshold // 10)
    elif dist <= 3 * threshold:
        return 15 + (dist - 2 * threshold) // (threshold // 4)
    else:
        return 19


def get_grad(val: np.ndarray) -> np.ndarray:
    return np.array([val[1], *(val[2:] - val[:-2]), -val[-2]])


def get_det(db: pd.DataFrame) -> np.ndarray:
    Pn_Po = np.array([db.x.iloc[-1] - db.x.iloc[0], db.y.iloc[-1] - db.y.iloc[0]])
    x0, y0 = db.x.iloc[0], db.y.iloc[0]
    det = np.array([np.linalg.det([Pn_Po, [x - x0, y - y0]])
                    for x, y in zip(db.x.iloc[1:].values, db.y.iloc[1:].values)])
    return det


# FEATURE EXTRACTION FUNCTION:

def direction_bin(db: pd.DataFrame, n_bin: int = 8) -> np.ndarray:
    grad_x, grad_y = get_grad(db.x.values), get_grad(db.y.values)
    direction = np.rad2deg(np.arctan2(grad_y, grad_x)) + 180
    direction = (direction % n_bin).astype(np.uint8)
    return np.argmax(np.bincount(direction))


@cached
def actual_distance(db: pd.DataFrame) -> float:
    return ((db.x.iloc[0] - db.x.iloc[-1]) ** 2 +
            (db.y.iloc[0] - db.y.iloc[-1]) ** 2) ** 0.5


def actual_distance_bin(db: pd.DataFrame, threshold: int = 250) -> int:
    return get_bin(int(actual_distance(db, cache=True)), threshold=threshold)


@cached
def curve_length(db: pd.DataFrame) -> float:
    return np.nansum(np.hypot(db.x.diff().values, db.y.diff().values))


def curve_length_bin(db: pd.DataFrame, threshold: int = 1000) -> int:
    return get_bin(int(curve_length(db, cache=True)), threshold=threshold)


def length_ratio(db: pd.DataFrame) -> float:
    ad = actual_distance(db, cache=True)
    return 0 if ad == 0 else curve_length(db, cache=True) / ad


def actual_speed(db: pd.DataFrame) -> float:
    dt = db.time.iloc[-1] - db.time.iloc[0]
    return 0 if dt == 0 else actual_distance(db, cache=True) / dt


@cached
def curve_speed(db: pd.DataFrame) -> float:
    dt = db.time.diff().values[1:]
    dt[dt == 0] = 1e-3
    return (np.hypot(db.x.diff().values[1:], db.y.diff().values[1:]) / dt).mean()


def curve_acceleration(db: pd.DataFrame) -> float:
    dt = db.time.iloc[-1] - db.time.iloc[0]
    return 0 if dt == 0 else curve_speed(db, cache=True) / dt


@cached
def mean_movement_offset(db: pd.DataFrame) -> float:
    Pn_Po = np.array([db.x.iloc[-1] - db.x.iloc[0], db.y.iloc[-1] - db.y.iloc[0]])
    norm = np.linalg.norm(Pn_Po)
    return 0 if norm == 0 else (get_det(db) / norm).mean()


def mean_movement_error(db: pd.DataFrame) -> float:
    Pn_Po = np.array([db.x.iloc[-1] - db.x.iloc[0], db.y.iloc[-1] - db.y.iloc[0]])
    norm = np.linalg.norm(Pn_Po)
    return 0 if norm == 0 else (np.abs(get_det(db) / norm)).mean()


def mean_movement_variability(db: pd.DataFrame) -> float:
    return ((db.y.iloc[1:-1] - mean_movement_offset(db, cache=True)) ** 2).mean() ** 0.5


@cached
def mean_curvature(db: pd.DataFrame) -> float:
    xy = np.hypot(db.x.values, db.y.values)
    mask = (xy != 0)
    return 0 if np.all(~mask) else\
        (np.arctan2(db.y, db.x)[mask] / xy[mask]).mean()


def mean_curvature_change_rate(db: pd.DataFrame) -> float:
    xy = ((db.x.iloc[-1] - db.x.iloc[:-1].values) ** 2 +
          (db.y.iloc[-1] - db.y.iloc[:-1].values) ** 2) ** 0.5
    mask = (xy != 0)
    return 0 if np.all(~mask) else\
        (np.arctan2(db.y.iloc[:-1].values, db.x.iloc[:-1].values)[mask] / xy[mask]).mean()


def mean_curvature_velocity(db: pd.DataFrame) -> float:
    dt = db.time.iloc[-1] - db.time.iloc[0]
    return 0 if dt == 0 else mean_curvature(db, cache=True)


def mean_curvature_velocity_change_rate(db: pd.DataFrame) -> float:
    dt = db.time.iloc[-1] - db.time.iloc[0]
    return 0 if dt == 0 else mean_curvature(db, cache=True) / (dt ** 2)


def mean_angular_velocity(db: pd.DataFrame) -> float:
    a = np.array([db.x.iloc[:-2].values - db.x.iloc[1:-1].values,
                  db.y.iloc[:-2].values - db.y.iloc[1:-1].values])
    b = np.array([db.x.iloc[2:].values - db.x.iloc[1:-1].values,
                  db.y.iloc[2:].values - db.y.iloc[1:-1].values])
    norm = np.linalg.norm(a, axis=0) * np.linalg.norm(b, axis=0)
    if np.all(norm == 0):
        return 0
    mask = (norm != 0)
    x = np.minimum(1, np.maximum(-1, np.sum(a * b, axis=0)[mask] / norm[mask]))
    angle = np.arccos(x)
    dt = (db.time.iloc[2:].values - db.time.iloc[:-2].values)[mask]
    dt[dt == 0] = 1e-3
    return (angle / dt).mean()

from config import (TRUST_MODEL_PARAMS, ONE_CLASS_SVM_PARAMS,
                    MIN_TRAIN_SIZE, TTIME_VALUE, DATA_PATH)
from src.pipeline.database import DataDB
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from math import exp
import numpy as np
import joblib
import time
import os


# link:
# https://joblib.readthedocs.io/en/latest/
# https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html
# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html


class TrustModel:
    def __init__(self,
                 user_id: int,
                 A: float = 0.00,
                 B: float = 0.25,
                 C: float = 1.00,
                 D: float = 1.00,
                 lockout: float = 90.0):
        """
        Dynamic Trust Model (DTM)

        :param user_id: User ID
        :param A: Threshold for penalty or reward, A > 0
        :param B: Width of the sigmoid,            B > 0
        :param C: Maximum reward,                  C > 0
        :param D: Maximum penalty,                 D > 0
        :param lockout: Minimum T-value after which blocking occurs
                        0 <= lockout <= T-value <= 100
        """
        self.A, self.B, self.C, self.D = A, B, C, D
        self.uid = user_id
        self.T_value = 100.0
        self.T_lockout = max(0.0, min(lockout, self.T_value))
        self.model_path = os.path.join(DATA_PATH, f"model_{user_id}.joblib")
        self.scaler_path = os.path.join(DATA_PATH, f"scaler_{user_id}.joblib")

        if os.path.exists(self.model_path) and \
                os.path.exists(self.scaler_path):
            self.scaler = joblib.load(filename=self.scaler_path)
            self.clf = joblib.load(filename=self.model_path)
            self.train = True
        else:
            self.scaler = StandardScaler()
            self.clf = OneClassSVM(**ONE_CLASS_SVM_PARAMS)
            self.train = False

    def fit(self, X, save: bool = True) -> "TrustModel":
        """
        Detects the soft boundary of the set of samples X.

        :param X: Set of samples
        :param save: dump model
        """
        X_transform = self.scaler.fit_transform(X)
        self.clf.fit(X_transform)
        self.train = True
        if save:
            joblib.dump(value=self.scaler, filename=self.scaler_path)
            joblib.dump(value=self.clf, filename=self.model_path)
        return self

    def predict(self, X: np.ndarray) -> float:
        """
        Signed distance to the separating hyperplane.
        Signed distance is positive for an inlier and negative for an outlier.

        :param X: Feature vector
        :return: classifier trust value
        """
        X_transform = self.scaler.transform(X.reshape(1, -1))
        return self.clf.decision_function(X_transform)

    def decision(self, X: np.ndarray) -> bool:
        """
        Recalculates the T-value and decides to block the user

        :param X: Feature vector
        :return: True, if the user's trust falls below the threshold
        """
        up = self.D * (1.0 + (1.0 / self.C))
        down = (1.0 / self.C) + exp(-(self.predict(X) - self.A) / self.B)
        delta_T = min(-self.D + up / down, self.C)
        self.T_value = min(max(self.T_value + delta_T, 0.0), 100.0)
        return self.T_value < self.T_lockout


model = None


def authentication(user_id: int, feature: np.ndarray) -> bool:
    """
    Verification of the user's biometric data.

    :param user_id: User ID
    :param feature: Feature vector
    :return: True, if the user has passed the authentication process
             False otherwise
    """
    global model
    if model is None:
        model = TrustModel(user_id, **TRUST_MODEL_PARAMS)

    db = DataDB(user_id)
    if model.train:
        prediction = model.decision(feature)
        if prediction and model.T_value == 100.0:
            db.add(list(feature))
        if not prediction:
            del model
            model = None
        return prediction

    # --- DEBUG
    db_size = db.get_train_data_size()
    t = time.gmtime(round((MIN_TRAIN_SIZE - db_size) * TTIME_VALUE))
    t = time.strftime('%H:%M:%S', t)
    print(f"Data [{db_size:<6}/{MIN_TRAIN_SIZE}] ~ "
          f"{t} left until the end of data collection",
          end='\r', flush=True)
    # ---

    if db_size < MIN_TRAIN_SIZE:
        db.add(list(feature))
    else:
        X = np.array(db.get_train_data())[:, 1:]
        model.fit(X)

    return True


if __name__ == "__main__":
    pass

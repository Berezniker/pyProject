from src.pipeline.database import DataDB
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from typing import Dict, Union
from config import DATA_PATH
from math import exp
import numpy as np
import logging
import joblib
import time
import os


# link:
# https://joblib.readthedocs.io/en/latest/
# https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html
# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html


class TrustModel:
    def __init__(
            self,
            user_id: int,
            A: float = 0.00,
            B: float = 0.25,
            C: float = 1.00,
            D: float = 1.00,
            lockout: float = 90.0,
            one_class_svm_params: Dict[str, Union[str, float]] = {}
    ):
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
            logging.info("Upload the trained model")
            self.scaler = joblib.load(filename=self.scaler_path)
            self.clf = joblib.load(filename=self.model_path)
            self.train = True
        else:
            logging.info("Create a new model")
            self.scaler = StandardScaler()
            self.clf = OneClassSVM(**one_class_svm_params)
            self.train = False

    def fit(self, X, save: bool = True) -> "TrustModel":
        """
        Detects the soft boundary of the set of samples X.

        :param X: Set of samples
        :param save: dump model
        """
        logging.info("Train the model")
        train_time = time.time()
        X_transform = self.scaler.fit_transform(X)
        self.clf.fit(X_transform)
        train_time = time.time() - train_time
        logging.info(f"Train time: {train_time}")
        self.train = True
        if save:
            logging.info("Save the trained model")
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
        return self.T_value > self.T_lockout


model = None


def authentication(user_id: int, feature: np.ndarray, args) -> bool:
    """
    Verification of the user's biometric data.

    :param user_id: User ID
    :param feature: Feature vector
    :param args: Command line arguments
    :return: True, if the user has passed the authentication process
             False otherwise
    """
    global model
    if model is None:
        model = TrustModel(
            user_id=user_id,
            A=args.trust_model_a,
            B=args.trust_model_b,
            C=args.trust_model_c,
            D=args.trust_model_d,
            lockout=args.trust_model_lockout,
            one_class_svm_params={
                "kernel": args.one_class_svm_kernel,
                "gamma": args.one_class_svm_gamma,
                "nu": args.one_class_svm_nu
            }
        )

    db = DataDB(user_id)
    if model.train:
        prediction = model.decision(feature)
        logging.debug(f"Model Trust value: {model.T_value:.5f}")
        if prediction and model.T_value == 100.0:
            db.add(list(feature))
        if not prediction:
            del model
            model = None
        return prediction

    # --- DEBUG
    db_size = db.get_train_data_size()
    t = time.gmtime(round((args.min_train_size - db_size) * args.ttime_value))
    t = time.strftime('%H:%M:%S', t)
    logging.debug(
        f"Data [{db_size:<6}/{args.min_train_size}] ~ "
        f"{t} left until the end of data collection"
    )
    # ---

    if db_size < args.min_train_size:
        db.add(list(feature))
    else:
        X = np.array(db.get_train_data())[:, 1:]
        model.fit(X)

    return True


if __name__ == "__main__":
    pass

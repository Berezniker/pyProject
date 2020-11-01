from config import TRUST_MODEL_PARAMS, ONE_CLASS_SVM_PARAMS, MIN_TRAIN_SIZE
from src.pipeline.database import DataDB
from sklearn.svm import OneClassSVM
from joblib import dump, load
from math import exp
import numpy as np

# link:
# https://joblib.readthedocs.io/en/latest/
# https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html


class TrustModel:
    def __init__(self,
                 A: float = 0.00,
                 B: float = 0.25,
                 C: float = 1.00,
                 D: float = 1.00,
                 lockout: float = 90.0):
        """
        Dynamic Trust Model (DTM)

        :param A: Threshold for penalty or reward, A > 0
        :param B: Width of the sigmoid,            B > 0
        :param C: Maximum reward,                  C > 0
        :param D: Maximum penalty,                 D > 0
        :param lockout: Minimum T-value after which blocking occurs
                        0 <= lockout <= T-value=100
        """
        self.A, self.B, self.C, self.D = A, B, C, D
        self.T_value = 100.0
        self.T_lockout = max(0.0, min(lockout, self.T_value))
        if False:
            self.clf = load("model.joblib")
        else:
            self.clf = OneClassSVM(**ONE_CLASS_SVM_PARAMS)
        self.train = False

    def fit(self, X, save: bool = False) -> "TrustModel":
        """
        Detects the soft boundary of the set of samples X.

        :param X: Set of samples
        :param save: dump model to
        """
        self.clf.fit(X)
        self.train = True
        if save:
            dump(self.clf, filename=f"model.joblib")
        return self

    def predict(self, X: np.ndarray) -> float:
        """
        Signed distance to the separating hyperplane.
        Signed distance is positive for an inlier and negative for an outlier.

        :param X: Feature vector
        :return: classifier trust value
        """
        return self.clf.decision_function(X.reshape(1, -1))

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

    def restart(self) -> None:
        """
        Sets the T-value to the maximum after re-authorization
        """
        self.T_value = 100.0
        return


model = TrustModel(**TRUST_MODEL_PARAMS)

def authentication(user_id: int, feature: np.ndarray) -> bool:
    db = DataDB(user_id)
    if model.train:
        prediction = model.decision(feature)
        if prediction and model.T_value == 100.0:
            db.add(list(feature))
        if not prediction:
            model.restart()  # for the feature
        return prediction

    if db.get_train_data_size() < MIN_TRAIN_SIZE:
        db.add(list(feature))
    else:
        X = np.array(db.get_train_data())[:, 1:]
        model.fit(X)

    return True


if __name__ == "__main__":
    pass

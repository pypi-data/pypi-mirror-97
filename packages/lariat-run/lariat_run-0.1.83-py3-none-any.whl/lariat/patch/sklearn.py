from lariat.patch.statsd_config import DEFAULT_STATSD_CLIENT as STATSD_CLIENT
from sklearn import model_selection
from sklearn import linear_model


_LogisticRegression = linear_model.LogisticRegression

_train_test_split = model_selection.train_test_split

sklearn_string = "sklearn.."
logreg_string = "logistic_regression.."


def train_test_split_patched(*args, **kwargs):
    """
    New train_test_split function
    """
    with STATSD_CLIENT.timer(f"{sklearn_string}train_test_split"):
        return _train_test_split(*args, **kwargs)


class PatchedLogisticRegression(_LogisticRegression):
    def predict_proba(self, X):
        with STATSD_CLIENT.timer(f"{sklearn_string}{logreg_string}predict_proba"):
            return super(PatchedLogisticRegression, self).predict_proba(X)

    def fit(self, X, y, sample_weight=None):
        with STATSD_CLIENT.timer(f"{sklearn_string}{logreg_string}fit"):
            return super(PatchedLogisticRegression, self).fit(X, y, sample_weight)


def patch():
    model_selection.train_test_split = train_test_split_patched
    linear_model.LogisticRegression = PatchedLogisticRegression

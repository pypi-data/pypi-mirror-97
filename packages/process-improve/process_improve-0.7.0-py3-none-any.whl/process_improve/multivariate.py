from sklearn.decomposition import PCA as PCA_sklearn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted

# We will specialize this class later on.
PCA = PCA_sklearn


# Create our own mean centering and scaling to unit variance (MCUV) class
# The default scaler in sklearn does not handle small datasets accurately, with ddof.
class MCUVScaler(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        self.center_x_ = X.mean()
        self.scale_x_ = X.std(
            ddof=1
        )  # this is the key difference with "preprocessing.StandardScaler"
        self.scale_x_[self.scale_x_ == 0] = 1.0  # columns with no variance are left as-is.
        return self

    def transform(self, X):
        check_is_fitted(self, "center_x_")
        check_is_fitted(self, "scale_x_")

        X = X.copy()
        return (X - self.center_x_) / self.scale_x_

    def inverse_transform(self, X):
        check_is_fitted(self, "center_x_")
        check_is_fitted(self, "scale_x_")

        X = X.copy()
        return X * self.scale_x_ + self.center_x_


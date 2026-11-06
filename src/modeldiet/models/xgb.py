from xgboost import XGBClassifier

from modeldiet.model import Model


class XGBoostModel(Model):
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 6,
        learning_rate: float = 0.3,
        subsample: float = 1.0,
        **kwargs,
    ):
        # Passes all telemetry tracking metrics straight to the base class
        super().__init__(**kwargs)

        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.subsample = subsample

        self.clf = XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            subsample=subsample,
        )

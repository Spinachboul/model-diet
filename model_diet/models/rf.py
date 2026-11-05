from model_diet.model import Model
from sklearn.ensemble import RandomForestClassifier

class RandomForestModel(Model):
    def __init__(self,
                 n_estimators: int=100,
                 max_depth: int=None, #type: ignore
                 **kwargs):
        super().__init__(**kwargs)

        # specific class configurations
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.clf = RandomForestClassifier(n_estimators=self.n_estimators, max_depth=self.max_depth)
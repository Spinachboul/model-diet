from model import Model
from sklearn.linear_model import LogisticRegression

class LogisticRegressionModel(Model):
    def __init__(self, C: float = 1.0, max_iter: int = 100, solver: str = 'lbfgs', **kwargs):
        # Passes all telemetry tracking arguments automatically to the base class
        super().__init__(**kwargs)
        
        self.C = C
        self.max_iter = max_iter
        self.solver = solver
        self.clf = LogisticRegression(C=C, max_iter=max_iter, solver=solver) #type: ignore
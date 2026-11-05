import time
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Model and reporting layout imports
from model import Model
from models.lr import LogisticRegressionModel
from models.rf import RandomForestModel
from models.xgb import XGBoostModel
from report import Report

def main():
    # 1. Load dataset
    data = load_breast_cancer(as_frame=True)
    X = data.data  # type: ignore
    y = data.target  # type: ignore

    # 2. Stratified split to maintain balance across train/test splits
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Handle Scaling (Required for Logistic Regression, benign for trees)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ==========================================
    # 4. Logistic Regression Evaluation
    # ==========================================
    print("Evaluating Logistic Regression...")
    lr_start = time.perf_counter()
    lr_model = LogisticRegressionModel(C=1.0, max_iter=1000)
    
    # Train using scaled data
    lr_model.clf.fit(X_train_scaled, y_train)
    
    # Measure latencies, process memory, and footprint sizes
    lr_model.profile_execution(X_test_scaled, load_start_time=lr_start)
    
    print("\nLogistic Regression Model Report:")
    lr_report = Report(lr_model, X_test_scaled, y_test)
    lr_report.print_report()

    # ==========================================
    # 5. Random Forest Evaluation
    # ==========================================
    print("\nEvaluating Random Forest...")
    rf_start = time.perf_counter()
    rf_model = RandomForestModel(n_estimators=100)
    
    # Tree algorithms don't strictly require scaling
    rf_model.clf.fit(X_train, y_train)
    rf_model.profile_execution(X_test, load_start_time=rf_start)
    
    print("\nRandom Forest Model Report:")
    rf_report = Report(rf_model, X_test, y_test)
    rf_report.print_report()

    # ==========================================
    # 6. XGBoost Evaluation
    # ==========================================
    print("\nEvaluating XGBoost...")
    xgb_start = time.perf_counter()
    xgb_model = XGBoostModel(n_estimators=100)
    
    xgb_model.clf.fit(X_train, y_train)
    xgb_model.profile_execution(X_test, load_start_time=xgb_start)
    
    print("\nXGBoost Model Report:")
    xgb_report = Report(xgb_model, X_test, y_test)
    xgb_report.print_report()


if __name__ == "__main__":
    main()

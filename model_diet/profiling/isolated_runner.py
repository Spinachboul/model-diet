import argparse
import json
import pickle
import sys
import tempfile
import time
import traceback
from pathlib import Path

from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from model_diet.models.lr import LogisticRegressionModel
from model_diet.models.rf import RandomForestModel
from model_diet.models.xgb import XGBoostModel
from model_diet.profiling.environment import EnvironmentMeasurement

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def create_model(model_name):
    """Create one of the estimators used by the repository demo."""
    if model_name == "lr":
        return LogisticRegressionModel(C=1.0, max_iter=1000)
    if model_name == "rf":
        return RandomForestModel(n_estimators=100, max_depth=None)
    if model_name == "xgb":
        return XGBoostModel(n_estimators=100, max_depth=6, learning_rate=0.3)
    raise ValueError(f"Unsupported model: {model_name}")


def load_dataset():
    """Load the example dataset and prepare train/test splits."""
    data = load_breast_cancer(as_frame=True)
    X, y = data.data, data.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test


def run_model(model_name, output_path):
    """Run one isolated demonstration benchmark and write JSON results."""
    print("\\n" + "=" * 60)
    print(f"STARTING ISOLATED PROCESS: {model_name.upper()}")
    print("=" * 60)

    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test = load_dataset()
    model = create_model(model_name)
    if model_name == "lr":
        train_data, test_data = X_train_scaled, X_test_scaled
    else:
        train_data, test_data = X_train, X_test

    training_start = time.perf_counter()
    model.clf.fit(train_data, y_train)
    training_time = time.perf_counter() - training_start
    print(f"\\nTraining Time: {training_time:.6f} seconds")

    # This measures pickle deserialization only, not process startup/imports.
    with tempfile.NamedTemporaryFile(suffix=".pkl") as temp_file:
        with open(temp_file.name, "wb") as file:
            pickle.dump(model.clf, file)
        load_start = time.perf_counter()
        with open(temp_file.name, "rb") as file:
            model.clf = pickle.load(file)
        model.loading_time = time.perf_counter() - load_start

    print(f"\\nModel Deserialization Time: {model.loading_time:.6f} seconds")

    # Each strategy executes its own experiment. Latency is never measured
    # while tracemalloc is active.
    measurements = model.profile_execution(test_data)
    predictions = model.clf.predict(test_data)
    accuracy = accuracy_score(y_test, predictions)
    environment = EnvironmentMeasurement().measure()

    results = {
        "model": model_name,
        "training_time": float(training_time),
        "loading_time": float(model.loading_time),
        "accuracy": float(accuracy),
        "mean_inference_latency": float(model.mean_inference_latency),
        "p50_latency": float(model.p50_latency),
        "p90_latency": float(model.p90_latency),
        "p95_latency": float(model.p95_latency),
        "p99_latency": float(model.p99_latency),
        "traced_peak_inference_allocation_mb": float(
            model.traced_peak_inference_allocation_mb
        ),
        "rss_after_inference_mb": float(model.rss_after_inference_mb),
        "serialized_model_size": float(model.serialized_model_size),
        "measurement_details": measurements,
        "environment": environment,
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as file:
        json.dump(results, file, indent=4)

    print("\\n" + "=" * 60)
    print(f"{model_name.upper()} MODEL REPORT")
    print("=" * 60)
    print(f"Accuracy                         : {accuracy * 100:.2f}%")
    print(f"Training Time                    : {training_time:.6f} sec")
    print(f"Model Deserialization Time       : {model.loading_time:.6f} sec")
    print(f"Mean Inference Latency           : {model.mean_inference_latency:.4f} ms")
    print(f"P99 Latency                      : {model.p99_latency:.4f} ms")
    print(
        "Traced Peak Inference Allocation: "
        f"{model.traced_peak_inference_allocation_mb:.4f} MB"
    )
    print(f"Process RSS After Inference      : {model.rss_after_inference_mb:.2f} MB")
    print(f"Serialized Model Size            : {model.serialized_model_size:.4f} MB")
    print("\\nResults saved to:", output_path)
    return results


def main():
    parser = argparse.ArgumentParser(description="Isolated ML Model Benchmark Runner")
    parser.add_argument(
        "--model", required=True, choices=["lr", "rf", "xgb"], help="Model to benchmark"
    )
    parser.add_argument("--output", required=True, help="JSON output file path")
    args = parser.parse_args()
    try:
        run_model(model_name=args.model, output_path=args.output)
    except Exception as error:
        print("\\nERROR:", str(error))
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

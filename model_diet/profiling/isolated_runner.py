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

# --------------------------------------------------
# PROJECT PATH CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# --------------------------------------------------
# MODEL FACTORY
# --------------------------------------------------


def create_model(model_name):

    if model_name == "lr":
        return LogisticRegressionModel(C=1.0, max_iter=1000)

    elif model_name == "rf":
        return RandomForestModel(n_estimators=100, max_depth=None)

    elif model_name == "xgb":
        return XGBoostModel(n_estimators=100, max_depth=6, learning_rate=0.3)

    else:
        raise ValueError(f"Unsupported model: {model_name}")


# --------------------------------------------------
# DATASET LOADING
# --------------------------------------------------


def load_dataset():

    data = load_breast_cancer(as_frame=True)

    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale only the data used by Logistic Regression.
    # Tree models retain their original DataFrame inputs.

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return (X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test)


# --------------------------------------------------
# MODEL EXECUTION
# --------------------------------------------------


def run_model(model_name, output_path):

    print("\n" + "=" * 60)
    print(f"STARTING ISOLATED PROCESS: {model_name.upper()}")
    print("=" * 60)

    # 1. Load dataset

    (X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test) = load_dataset()

    # 2. Create model

    model = create_model(model_name)

    # 3. Select appropriate dataset

    if model_name == "lr":

        train_data = X_train_scaled
        test_data = X_test_scaled

    else:

        train_data = X_train
        test_data = X_test

    # 4. Measure training time

    training_start = time.perf_counter()

    model.clf.fit(train_data, y_train)

    training_end = time.perf_counter()

    training_time = training_end - training_start

    print(f"\nTraining Time: {training_time:.6f} seconds")

    # save and reload trained model to measure the loading time
    with tempfile.NamedTemporaryFile(suffix=".pkl") as temp_file:
        with open(temp_file.name, "wb") as file:
            pickle.dump(model.clf, file)

        load_start_time = time.perf_counter()

        with open(temp_file.name, "rb") as file:
            model.clf = pickle.load(file)

        load_end_time = time.perf_counter()

        model.loading_time = load_end_time - load_start_time

    print(f"\nModel Loading Time: {model.loading_time:.6f}")

    # 5. Measure actual model serialization size
    # and profile inference

    model.profile_execution(
        test_data,
    )

    # 6. Calculate accuracy separately
    # so it does not affect inference latency measurements.

    predictions = model.clf.predict(test_data)

    accuracy = accuracy_score(y_test, predictions)

    # 7. Prepare benchmark results

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
        "traced_peak_memory_usage": float(model.traced_peak_memory_usage),
        "processed_rss": float(model.processed_rss),
        "serialized_model_size": float(model.serialized_model_size),
    }

    # 8. Save JSON results

    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as file:

        json.dump(results, file, indent=4)

    # 9. Display report

    print("\n" + "=" * 60)
    print(f"{model_name.upper()} MODEL REPORT")
    print("=" * 60)

    print(f"Accuracy              : {accuracy * 100:.2f}%")
    print(f"Training Time         : {training_time:.6f} sec")
    print(f"Loading Time          : {model.loading_time:.6f} sec")

    print(f"Mean Inference Latency: " f"{model.mean_inference_latency:.4f} ms")

    print(f"P99 Latency           : " f"{model.p99_latency:.4f} ms")

    print(f"Traced Peak Memory    : " f"{model.traced_peak_memory_usage:.4f} MB")

    print(f"RSS Memory            : " f"{model.processed_rss:.2f} MB")

    print(f"Serialized Size       : " f"{model.serialized_model_size:.4f} MB")

    print("\nResults saved to:", output_path)

    print("\n" + "=" * 60)
    print(f"COMPLETED: {model_name.upper()}")
    print("=" * 60)

    return results


# --------------------------------------------------
# MAIN ENTRY POINT
# --------------------------------------------------


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

        print("\nERROR:", str(error))

        traceback.print_exc()

        sys.exit(1)


if __name__ == "__main__":
    main()

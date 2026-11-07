from __future__ import annotations

import argparse
import json
import pickle
import tempfile
import time
import traceback
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Protocol

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from modeldiet import profile
from modeldiet.profiling import (
    LatencyMeasurement,
    ProcessRSSMeasurement,
    SerializationMeasurement,
    TracedAllocationMeasurement,
)


class _Estimator(Protocol):
    def fit(self, X: Any, y: Any) -> Any: ...

    def predict(self, X: Any) -> Any: ...


def create_model(model_name: str) -> _Estimator:
    """Create one of the estimators used by the repository demonstration."""
    if model_name == "lr":
        return LogisticRegression(C=1.0, max_iter=1000)
    if model_name == "rf":
        return RandomForestClassifier(n_estimators=100, max_depth=None)
    if model_name == "xgb":
        try:
            from xgboost import XGBClassifier
        except ModuleNotFoundError as exc:
            if exc.name != "xgboost":
                raise
            raise ImportError(
                "The XGBoost benchmark requires the optional dependency. "
                'Install it with `python -m pip install "modeldiet[benchmark-xgboost]"`.'
            ) from exc

        return XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.3)
    raise ValueError(f"Unsupported model: {model_name}")


def load_dataset() -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    NDArray[np.float64],
    NDArray[np.float64],
    pd.Series[Any],
    pd.Series[Any],
]:
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


def run_model(model_name: str, output_path: str | Path) -> Mapping[str, Any]:
    """Run one isolated demonstration benchmark and write JSON results."""
    print("\n" + "=" * 60)
    print(f"STARTING ISOLATED PROCESS: {model_name.upper()}")
    print("=" * 60)

    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test = load_dataset()
    model = create_model(model_name)
    train_data: pd.DataFrame | NDArray[np.float64]
    test_data: pd.DataFrame | NDArray[np.float64]
    if model_name == "lr":
        train_data, test_data = X_train_scaled, X_test_scaled
    else:
        train_data, test_data = X_train, X_test

    training_start = time.perf_counter()
    model.fit(train_data, y_train)
    training_time = time.perf_counter() - training_start
    print(f"\nTraining Time: {training_time:.6f} seconds")

    # This measures pickle deserialization only, not process startup/imports.
    with tempfile.NamedTemporaryFile(suffix=".pkl") as temp_file:
        with open(temp_file.name, "wb") as model_writer:
            pickle.dump(model, model_writer)
        load_start = time.perf_counter()
        with open(temp_file.name, "rb") as model_reader:
            # This is a round-trip of the pickle written from the in-memory
            # estimator above; the input is not user-controlled.
            model = pickle.load(model_reader)  # nosec B301
        loading_time = time.perf_counter() - load_start

    print(f"\nModel Deserialization Time: {loading_time:.6f} seconds")

    result = profile(
        model,
        test_data,
        measurements=[
            LatencyMeasurement(),
            TracedAllocationMeasurement(),
            ProcessRSSMeasurement(),
            SerializationMeasurement(),
        ],
        include_environment=True,
    )
    predictions = model.predict(test_data)
    accuracy = accuracy_score(y_test, predictions)

    def values(name: str) -> dict[str, Any]:
        return {
            key: metric.value
            for key, metric in result.measurements[name].metrics.items()
        }

    latency = values("latency")
    allocation = values("python_traced_allocation")
    process_memory = values("process_rss")
    serialization = values("pickle_size")
    measurement_details = {
        "latency": latency,
        "allocation": allocation,
        "process_memory": process_memory,
        "serialization": serialization,
    }

    results: dict[str, Any] = {
        "model": model_name,
        "training_time": float(training_time),
        "loading_time": float(loading_time),
        "accuracy": float(accuracy),
        "mean_inference_latency": float(latency["mean_ms"]),
        "p50_latency": float(latency["p50_ms"]),
        "p90_latency": float(latency["p90_ms"]),
        "p95_latency": float(latency["p95_ms"]),
        "p99_latency": float(latency["p99_ms"]),
        "traced_peak_inference_allocation_mb": float(
            allocation["traced_peak_inference_allocation_mb"]
        ),
        "rss_before_inference_mb": float(process_memory["rss_before_inference_mb"]),
        "rss_after_inference_mb": float(process_memory["rss_after_inference_mb"]),
        "rss_delta_mb": float(process_memory["rss_delta_mb"]),
        "serialized_model_size": float(serialization["serialized_model_size_mb"]),
        "measurement_details": measurement_details,
        "environment": result.environment,
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(results, output_file, indent=4)

    print("\n" + "=" * 60)
    print(f"{model_name.upper()} MODEL REPORT")
    print("=" * 60)
    print(f"Accuracy                         : {accuracy * 100:.2f}%")
    print(f"Training Time                    : {training_time:.6f} sec")
    print(f"Model Deserialization Time       : {loading_time:.6f} sec")
    print(f"Mean Inference Latency           : {latency['mean_ms']:.4f} ms")
    print(f"P99 Latency                      : {latency['p99_ms']:.4f} ms")
    print(
        "Traced Peak Inference Allocation: "
        f"{allocation['traced_peak_inference_allocation_mb']:.4f} MB"
    )
    print(
        "Process RSS Before / After     : "
        f"{process_memory['rss_before_inference_mb']:.2f} / "
        f"{process_memory['rss_after_inference_mb']:.2f} MB"
    )
    print(f"Process RSS Delta                : {process_memory['rss_delta_mb']:.4f} MB")
    print(
        "Pickle Serialized Model Size   : "
        f"{serialization['serialized_model_size_mb']:.4f} MB"
    )
    print("\nResults saved to:", output_path)
    return results


def main() -> None:
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
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()

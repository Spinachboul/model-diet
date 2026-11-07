import json
from unittest.mock import patch

import numpy as np

from modeldiet.benchmark import worker
from modeldiet.profiling.isolated_runner import run_model


class DummyClassifier:
    def fit(self, X, y):
        self.class_value = int(y[0])
        return self

    def predict(self, X):
        return np.full(len(X), self.class_value, dtype=int)


def _make_dataset():
    X_train = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]])
    X_test = np.array([[9.0, 10.0], [11.0, 12.0]])
    y_train = np.array([0, 0, 1, 1])
    y_test = np.array([0, 1])
    return X_train, X_test, X_train, X_test, y_train, y_test


def _run_dummy_benchmark(tmp_path):
    output_path = tmp_path / "result.json"
    with (
        patch.object(worker, "create_model", return_value=DummyClassifier()),
        patch.object(worker, "load_dataset", return_value=_make_dataset()),
    ):
        result = run_model("lr", output_path)
    return result, output_path


def test_training_and_deserialization_times_are_recorded(tmp_path):
    results, _ = _run_dummy_benchmark(tmp_path)

    assert results["training_time"] >= 0
    assert results["loading_time"] >= 0


def test_accuracy_and_measurements_come_from_core_profile(tmp_path):
    results, _ = _run_dummy_benchmark(tmp_path)

    assert results["accuracy"] == 0.5
    assert results["model"] == "lr"
    assert results["measurement_details"]["latency"]["sample_count"] == 2
    assert results["measurement_details"]["latency"]["mean_ms"] >= 0
    assert (
        results["measurement_details"]["allocation"][
            "traced_peak_inference_allocation_mb"
        ]
        >= 0
    )
    assert (
        results["measurement_details"]["serialization"]["serialization_format"]
        == "pickle"
    )


def test_output_json_retains_benchmark_report_fields(tmp_path):
    results, output_path = _run_dummy_benchmark(tmp_path)

    saved_results = json.loads(output_path.read_text(encoding="utf-8"))
    expected_fields = {
        "model",
        "training_time",
        "loading_time",
        "accuracy",
        "mean_inference_latency",
        "p50_latency",
        "p90_latency",
        "p95_latency",
        "p99_latency",
        "traced_peak_inference_allocation_mb",
        "rss_before_inference_mb",
        "rss_after_inference_mb",
        "rss_delta_mb",
        "serialized_model_size",
        "measurement_details",
        "environment",
    }
    assert expected_fields.issubset(saved_results)
    assert saved_results == results
    assert saved_results["environment"]["python_version"]

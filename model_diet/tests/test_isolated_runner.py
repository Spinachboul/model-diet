import json
from unittest.mock import patch

import numpy as np

from model_diet.profiling.isolated_runner import run_model


class DummyClassifier:
    def fit(self, X, y):
        return self

    def predict(self, X):
        return np.zeros(len(X), dtype=int)


def _make_dummy_model():
    class DummyModel:
        def __init__(self):
            self.clf = DummyClassifier()
            self.loading_time = 0.0
            self.mean_inference_latency = 0.5
            self.p50_latency = 0.4
            self.p90_latency = 0.6
            self.p95_latency = 0.7
            self.p99_latency = 0.8
            self.traced_peak_inference_allocation_mb = 1.0
            self.rss_before_inference_mb = 99.0
            self.rss_after_inference_mb = 100.0
            self.rss_delta_mb = 1.0
            self.serialized_model_size = 0.01

        def profile_execution(self, test_data):
            return {
                "latency": {"mean_ms": self.mean_inference_latency},
                "allocation": {
                    "traced_peak_inference_allocation_mb": 1.0,
                },
                "process_memory": {
                    "rss_before_inference_mb": 99.0,
                    "rss_after_inference_mb": 100.0,
                    "rss_delta_mb": 1.0,
                },
                "serialization": {"serialized_model_size_mb": 0.01},
            }

    return DummyModel()


def _make_dataset():
    X_train = np.array([[1, 2], [3, 4], [5, 6]])
    X_test = np.array([[7, 8], [9, 10]])
    y_train = np.array([0, 1, 0])
    y_test = np.array([0, 0])
    return X_train, X_test, X_train, X_test, y_train, y_test


def test_loading_time_is_recorded(tmp_path):
    model = _make_dummy_model()
    with patch(
        "model_diet.profiling.isolated_runner.create_model", return_value=model
    ), patch(
        "model_diet.profiling.isolated_runner.load_dataset", return_value=_make_dataset()
    ), patch(
        "model_diet.profiling.isolated_runner.EnvironmentMeasurement.measure",
        return_value={"python_version": "test"},
    ):
        results = run_model("lr", tmp_path / "result.json")
    assert results["loading_time"] >= 0
    assert model.loading_time == results["loading_time"]


def test_training_time_is_recorded(tmp_path):
    model = _make_dummy_model()
    with patch(
        "model_diet.profiling.isolated_runner.create_model", return_value=model
    ), patch(
        "model_diet.profiling.isolated_runner.load_dataset", return_value=_make_dataset()
    ), patch(
        "model_diet.profiling.isolated_runner.EnvironmentMeasurement.measure",
        return_value={"python_version": "test"},
    ):
        results = run_model("lr", tmp_path / "result.json")
    assert results["training_time"] >= 0


def test_accuracy_is_valid(tmp_path):
    model = _make_dummy_model()
    with patch(
        "model_diet.profiling.isolated_runner.create_model", return_value=model
    ), patch(
        "model_diet.profiling.isolated_runner.load_dataset", return_value=_make_dataset()
    ), patch(
        "model_diet.profiling.isolated_runner.EnvironmentMeasurement.measure",
        return_value={"python_version": "test"},
    ):
        results = run_model("lr", tmp_path / "result.json")
    assert 0.0 <= results["accuracy"] <= 1.0


def test_output_json_contains_explicit_measurements(tmp_path):
    model = _make_dummy_model()
    output_path = tmp_path / "result.json"
    with patch(
        "model_diet.profiling.isolated_runner.create_model", return_value=model
    ), patch(
        "model_diet.profiling.isolated_runner.load_dataset", return_value=_make_dataset()
    ), patch(
        "model_diet.profiling.isolated_runner.EnvironmentMeasurement.measure",
        return_value={"python_version": "test"},
    ):
        results = run_model("lr", output_path)

    assert output_path.exists()
    with open(output_path, "r") as file:
        saved_results = json.load(file)
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
    assert expected_fields.issubset(saved_results.keys())
    assert saved_results == results
    assert saved_results["model"] == "lr"

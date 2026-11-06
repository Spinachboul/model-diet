import json
from unittest.mock import patch

import numpy as np
import pytest  # type: ignore

from model_diet.profiling.isolated_runner import run_model


class DummyClassifier:
    def fit(self, X, y):
        return self

    def predict(self, X):
        return np.zeros(len(X), dtype=int)


@pytest.fixture
def mock_model():
    """Create a lightweight model with the attributes expected by the runner."""

    class DummyModel:
        def __init__(self):
            self.clf = DummyClassifier()

            self.loading_time = 0.0
            self.mean_inference_latency = 0.5
            self.p50_latency = 0.4
            self.p90_latency = 0.6
            self.p95_latency = 0.7
            self.p99_latency = 0.8
            self.traced_peak_memory_usage = 1.0
            self.processed_rss = 100.0
            self.serialized_model_size = 0.01

        def profile_execution(self, test_data):
            pass

    return DummyModel()


@pytest.fixture
def mock_dataset():
    """Provide deterministic training and test data."""

    X_train = np.array([[1, 2], [3, 4], [5, 6]])
    X_test = np.array([[7, 8], [9, 10]])

    y_train = np.array([0, 1, 0])
    y_test = np.array([0, 0])

    return (
        X_train,
        X_test,
        X_train,
        X_test,
        y_train,
        y_test,
    )


@pytest.fixture
def patched_runner(mock_model, mock_dataset):
    """Patch model creation and dataset loading."""

    with (
        patch(
            "model_diet.profiling.isolated_runner.create_model",
            return_value=mock_model,
        ),
        patch(
            "model_diet.profiling.isolated_runner.load_dataset",
            return_value=mock_dataset,
        ),
    ):
        yield mock_model


def test_loading_time_is_recorded(tmp_path, patched_runner):
    """Loading time should be populated and non-negative."""

    output_path = tmp_path / "result.json"

    results = run_model("lr", output_path)

    assert results["loading_time"] >= 0
    assert patched_runner.loading_time == results["loading_time"]


def test_training_time_is_recorded(tmp_path, patched_runner):
    """Training time should be populated and non-negative."""

    output_path = tmp_path / "result.json"

    results = run_model("lr", output_path)

    assert results["training_time"] >= 0


def test_accuracy_is_valid(tmp_path, patched_runner):
    """Accuracy should be between zero and one."""

    output_path = tmp_path / "result.json"

    results = run_model("lr", output_path)

    assert 0.0 <= results["accuracy"] <= 1.0


def test_output_json_contains_expected_fields(tmp_path, patched_runner):
    """The runner should create valid JSON with all expected metrics."""

    output_path = tmp_path / "result.json"

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
        "traced_peak_memory_usage",
        "processed_rss",
        "serialized_model_size",
    }

    assert expected_fields.issubset(saved_results.keys())
    assert saved_results == results
    assert saved_results["model"] == "lr"

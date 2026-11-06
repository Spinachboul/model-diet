import numpy as np
import pytest

from modeldiet.model import Model
from modeldiet.profiling.measurements import (
    BaseMeasurement,
    LatencyMeasurement,
    ProcessRSSMeasurement,
    SerializationMeasurement,
    TracedAllocationMeasurement,
)


class DummyEstimator:
    def predict(self, X):
        return np.zeros(len(X), dtype=int)


class FixedMeasurement(BaseMeasurement):
    """Small test strategy used to verify Model dependency injection."""

    def __init__(self, result):
        self.result = result
        self.calls = 0

    def measure(self, model, X=None):
        self.calls += 1
        return self.result


def test_latency_measurement_returns_percentiles():
    X = np.ones((5, 3))
    result = LatencyMeasurement(warmup_iterations=1).measure(DummyEstimator(), X)
    assert result["sample_count"] == 5
    assert result["mean_ms"] >= 0
    assert result["p50_ms"] >= 0
    assert result["p99_ms"] >= 0


def test_latency_measurement_rejects_empty_input():
    with pytest.raises(ValueError, match="at least one sample"):
        LatencyMeasurement().measure(DummyEstimator(), np.empty((0, 3)))


def test_latency_measurement_rejects_non_2d_input():
    with pytest.raises(ValueError, match="2D"):
        LatencyMeasurement().measure(DummyEstimator(), np.ones(3))


def test_traced_allocation_measurement_runs_without_latency_timer():
    result = TracedAllocationMeasurement().measure(DummyEstimator(), np.ones((5, 3)))
    assert result["traced_peak_inference_allocation_mb"] >= 0


def test_process_rss_measurement_returns_before_after_and_delta():
    result = ProcessRSSMeasurement().measure(DummyEstimator(), np.ones((5, 3)))
    assert result["rss_before_inference_mb"] > 0
    assert result["rss_after_inference_mb"] > 0
    assert result["rss_delta_mb"] == pytest.approx(
        result["rss_after_inference_mb"] - result["rss_before_inference_mb"]
    )


def test_serialization_measurement_works_without_input():
    result = SerializationMeasurement().measure(DummyEstimator())
    assert result["serialized_model_size_mb"] > 0
    assert result["serialization_format"] == "pickle"


def test_measurement_classes_support_subclassing():
    class CustomLatencyMeasurement(LatencyMeasurement):
        pass

    assert isinstance(CustomLatencyMeasurement(), LatencyMeasurement)


def test_model_accepts_custom_measurement_objects():
    latency = FixedMeasurement(
        {
            "mean_ms": 1.0,
            "p50_ms": 0.9,
            "p90_ms": 1.1,
            "p95_ms": 1.2,
            "p99_ms": 1.5,
            "sample_count": 4,
        }
    )
    allocation = FixedMeasurement({"traced_peak_inference_allocation_mb": 2.0})
    rss = FixedMeasurement(
        {
            "rss_before_inference_mb": 50.0,
            "rss_after_inference_mb": 51.0,
            "rss_delta_mb": 1.0,
        }
    )
    serialization = FixedMeasurement(
        {"serialized_model_size_mb": 0.25, "serialization_format": "test"}
    )
    model = Model(
        latency_measurement=latency,
        allocation_measurement=allocation,
        rss_measurement=rss,
        serialization_measurement=serialization,
    )
    model.clf = DummyEstimator()

    result = model.profile_execution(np.ones((4, 2)))

    assert list(result) == [
        "latency",
        "allocation",
        "process_memory",
        "serialization",
    ]
    assert model.mean_inference_latency == 1.0
    assert model.traced_peak_inference_allocation_mb == 2.0
    assert model.rss_after_inference_mb == 51.0
    assert model.rss_delta_mb == 1.0
    assert model.serialized_model_size == 0.25
    assert all(
        strategy.calls == 1 for strategy in (latency, allocation, rss, serialization)
    )

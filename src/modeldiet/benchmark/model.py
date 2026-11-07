"""Model wrapper that delegates profiling to independent measurements."""

from __future__ import annotations

import warnings
from typing import Any

from modeldiet import profile
from modeldiet.profiling.measurements import (
    BaseMeasurement,
    LatencyMeasurement,
    ProcessRSSMeasurement,
    SerializationMeasurement,
    TracedAllocationMeasurement,
)


class _NamedMeasurement(BaseMeasurement):
    """Give a legacy strategy slot a stable name for the core profile API."""

    def __init__(self, name: str, measurement: BaseMeasurement) -> None:
        self.name = name
        self.measurement = measurement

    def measure(self, model: Any, X: Any = None) -> dict[str, Any]:
        return self.measurement.measure(model, X)


class Model:
    """Compatibility wrapper around a trained estimator.

    Estimator-specific subclasses provide ``clf``. Measurement strategies are
    independent objects that can be reused, injected, or subclassed by callers.
    """

    def __init__(
        self,
        loading_time: float = 0.0,
        mean_inference_latency: float = 0.0,
        p50_latency: float = 0.0,
        p90_latency: float = 0.0,
        p95_latency: float = 0.0,
        p99_latency: float = 0.0,
        traced_peak_memory_usage: float = 0.0,
        processed_rss: float = 0.0,
        serialized_model_size: float = 0.0,
        latency_measurement: BaseMeasurement | None = None,
        allocation_measurement: BaseMeasurement | None = None,
        rss_measurement: BaseMeasurement | None = None,
        serialization_measurement: BaseMeasurement | None = None,
    ) -> None:
        warnings.warn(
            f"{type(self).__name__} is a deprecated benchmark compatibility "
            "interface. Use an ordinary fitted estimator with "
            "modeldiet.profile(estimator, X) instead. The legacy model "
            "interfaces will remain available through the 0.x series and "
            "will not be removed before 1.0.0.",
            DeprecationWarning,
            stacklevel=3 if type(self) is not Model else 2,
        )
        self.loading_time = loading_time
        self.mean_inference_latency = mean_inference_latency
        self.p50_latency = p50_latency
        self.p90_latency = p90_latency
        self.p95_latency = p95_latency
        self.p99_latency = p99_latency
        self.traced_peak_inference_allocation_mb = traced_peak_memory_usage
        self.rss_before_inference_mb = processed_rss
        self.rss_after_inference_mb = processed_rss
        self.rss_delta_mb = 0.0
        self.traced_peak_memory_usage = traced_peak_memory_usage  # compatibility
        self.processed_rss = processed_rss  # compatibility
        self.serialized_model_size = serialized_model_size

        self.clf: Any = None
        self.latency_measurement = (
            latency_measurement
            if latency_measurement is not None
            else LatencyMeasurement()
        )
        self.allocation_measurement = (
            allocation_measurement
            if allocation_measurement is not None
            else TracedAllocationMeasurement()
        )
        self.rss_measurement = (
            rss_measurement if rss_measurement is not None else ProcessRSSMeasurement()
        )
        self.serialization_measurement = (
            serialization_measurement
            if serialization_measurement is not None
            else SerializationMeasurement()
        )

    def profile_execution(
        self, X_test: Any, load_start_time: float | None = None
    ) -> dict[str, dict[str, Any]]:
        """Run each measurement through the core profiling API.

        ``load_start_time`` remains accepted for backwards compatibility. An
        already-loaded model has no measurable historical load duration.
        """
        del load_start_time
        named_measurements = [
            _NamedMeasurement("latency", self.latency_measurement),
            _NamedMeasurement("python_traced_allocation", self.allocation_measurement),
            _NamedMeasurement("process_rss", self.rss_measurement),
            _NamedMeasurement("pickle_size", self.serialization_measurement),
        ]
        result = profile(self.clf, X_test, measurements=named_measurements)

        def values(name: str) -> dict[str, Any]:
            return {
                key: metric.value
                for key, metric in result.measurements[name].metrics.items()
            }

        latency = values("latency")
        allocation = values("python_traced_allocation")
        process_memory = values("process_rss")
        serialization = values("pickle_size")

        self.mean_inference_latency = latency["mean_ms"]
        self.p50_latency = latency["p50_ms"]
        self.p90_latency = latency["p90_ms"]
        self.p95_latency = latency["p95_ms"]
        self.p99_latency = latency["p99_ms"]
        self.traced_peak_inference_allocation_mb = allocation[
            "traced_peak_inference_allocation_mb"
        ]
        self.rss_before_inference_mb = process_memory["rss_before_inference_mb"]
        self.rss_after_inference_mb = process_memory["rss_after_inference_mb"]
        self.rss_delta_mb = process_memory["rss_delta_mb"]
        self.traced_peak_memory_usage = self.traced_peak_inference_allocation_mb
        self.processed_rss = self.rss_after_inference_mb
        self.serialized_model_size = serialization["serialized_model_size_mb"]

        return {
            "latency": latency,
            "allocation": allocation,
            "process_memory": process_memory,
            "serialization": serialization,
        }

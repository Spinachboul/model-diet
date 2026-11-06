"""Model wrapper that delegates profiling to independent measurements."""

from __future__ import annotations

from typing import Any

from model_diet.profiling.measurements import (
    BaseMeasurement,
    LatencyMeasurement,
    ProcessRSSMeasurement,
    SerializationMeasurement,
    TracedAllocationMeasurement,
)


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
        """Run each measurement as an independent experiment.

        ``load_start_time`` remains accepted for backwards compatibility. An
        already-loaded model has no measurable historical load duration.
        """
        del load_start_time
        latency = self.latency_measurement.measure(self.clf, X_test)
        allocation = self.allocation_measurement.measure(self.clf, X_test)
        process_memory = self.rss_measurement.measure(self.clf, X_test)
        serialization = self.serialization_measurement.measure(self.clf)

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

"""Model wrapper that delegates profiling to independent measurements."""
from __future__ import annotations

from typing import Any

from model_diet.profiling.measurements import (
    LatencyMeasurement,
    MemoryMeasurement,
    SerializationMeasurement,
)


class Model:
    """Compatibility wrapper around a trained estimator.

    Estimator-specific subclasses provide ``clf``. Measurement strategies are
    independent objects that can be reused or subclassed without inheriting
    from this wrapper.
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
    ) -> None:
        # Loading time is retained for compatibility with the demo runner.
        # It must represent a timed artifact deserialization operation.
        self.loading_time = loading_time
        self.mean_inference_latency = mean_inference_latency
        self.p50_latency = p50_latency
        self.p90_latency = p90_latency
        self.p95_latency = p95_latency
        self.p99_latency = p99_latency
        self.traced_peak_inference_allocation_mb = traced_peak_memory_usage
        self.rss_after_inference_mb = processed_rss
        self.traced_peak_memory_usage = traced_peak_memory_usage  # compatibility
        self.processed_rss = processed_rss  # compatibility
        self.serialized_model_size = serialized_model_size

        self.clf: Any = None
        self.measurements = (
            LatencyMeasurement(),
            MemoryMeasurement(),
            SerializationMeasurement(),
        )

    def profile_execution(
        self, X_test: Any, load_start_time: float | None = None
    ) -> dict[str, dict[str, Any]]:
        """Run latency, memory, and serialization measurements independently.

        ``load_start_time`` is accepted for backwards compatibility only. An
        already-loaded model has no measurable historical load duration; callers
        should time deserialization at the point where it occurs.
        """
        del load_start_time
        latency = self.measurements[0].measure(self.clf, X_test)
        memory = self.measurements[1].measure(self.clf, X_test)
        serialization = self.measurements[2].measure(self.clf)

        self.mean_inference_latency = latency["mean_ms"]
        self.p50_latency = latency["p50_ms"]
        self.p90_latency = latency["p90_ms"]
        self.p95_latency = latency["p95_ms"]
        self.p99_latency = latency["p99_ms"]

        self.traced_peak_inference_allocation_mb = memory[
            "traced_peak_inference_allocation_mb"
        ]
        self.rss_after_inference_mb = memory["rss_after_inference_mb"]
        # Preserve attributes consumed by older report code for this transition.
        self.traced_peak_memory_usage = self.traced_peak_inference_allocation_mb
        self.processed_rss = self.rss_after_inference_mb
        self.serialized_model_size = serialization["serialized_model_size_mb"]

        return {
            "latency": latency,
            "memory": memory,
            "serialization": serialization,
        }

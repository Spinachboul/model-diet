"""Reusable measurement strategies for trained estimators.

Each strategy accepts an estimator rather than a Model Diet wrapper, making
the classes reusable with other callers and straightforward to subclass.
"""
from __future__ import annotations

import pickle
import time
import tracemalloc
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import psutil


class BaseMeasurement(ABC):
    """Base interface for an individual model measurement."""

    @abstractmethod
    def measure(self, model: Any, X: Any = None) -> dict[str, Any]:
        """Measure one property of a model."""


def _as_samples(X: Any) -> np.ndarray:
    """Convert pandas/array input to a validated 2D NumPy array."""
    values = X.to_numpy() if hasattr(X, "to_numpy") else np.asarray(X)
    values = np.asarray(values)
    if values.ndim != 2:
        raise ValueError("X must be 2D with shape (n_samples, n_features)")
    if values.shape[0] == 0:
        raise ValueError("X must contain at least one sample")
    return values


@dataclass(frozen=True)
class LatencyMetrics:
    """Single-sample prediction latency distribution, in milliseconds."""

    mean_ms: float
    p50_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float
    sample_count: int


class LatencyMeasurement(BaseMeasurement):
    """Measure per-sample prediction latency without tracemalloc enabled."""

    def __init__(self, warmup_iterations: int = 1) -> None:
        if warmup_iterations < 0:
            raise ValueError("warmup_iterations must be non-negative")
        self.warmup_iterations = warmup_iterations

    def measure(self, model: Any, X: Any = None) -> dict[str, Any]:
        samples = _as_samples(X)
        for _ in range(self.warmup_iterations):
            model.predict(samples[0:1])

        latencies = []
        for sample in samples:
            sample_input = sample.reshape(1, -1)
            start = time.perf_counter()
            model.predict(sample_input)
            latencies.append((time.perf_counter() - start) * 1000.0)

        values = np.asarray(latencies, dtype=float)
        return asdict(
            LatencyMetrics(
                mean_ms=float(np.mean(values)),
                p50_ms=float(np.percentile(values, 50)),
                p90_ms=float(np.percentile(values, 90)),
                p95_ms=float(np.percentile(values, 95)),
                p99_ms=float(np.percentile(values, 99)),
                sample_count=int(values.size),
            )
        )


@dataclass(frozen=True)
class MemoryMetrics:
    """Python allocation peak and a process-wide RSS snapshot."""

    traced_peak_inference_allocation_mb: float
    rss_after_inference_mb: float


class MemoryMeasurement(BaseMeasurement):
    """Measure allocations separately from latency and capture process RSS.

    RSS is for the entire process, not model-only memory or peak RSS.
    """

    def measure(self, model: Any, X: Any = None) -> dict[str, Any]:
        samples = _as_samples(X)
        if tracemalloc.is_tracing():
            raise RuntimeError("tracemalloc is already active in this process")

        tracemalloc.start()
        try:
            for sample in samples:
                model.predict(sample.reshape(1, -1))
            _, peak_bytes = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()

        rss_bytes = psutil.Process().memory_info().rss
        return asdict(
            MemoryMetrics(
                traced_peak_inference_allocation_mb=float(
                    peak_bytes / (1024.0 * 1024.0)
                ),
                rss_after_inference_mb=float(rss_bytes / (1024.0 * 1024.0)),
            )
        )


@dataclass(frozen=True)
class SerializationMetrics:
    """Serialized artifact size and format."""

    serialized_model_size_mb: float
    serialization_format: str


class SerializationMeasurement(BaseMeasurement):
    """Measure the size of a Python-pickle representation of a model."""

    def measure(self, model: Any, X: Any = None) -> dict[str, Any]:
        del X
        serialized = pickle.dumps(model)
        return asdict(
            SerializationMetrics(
                serialized_model_size_mb=float(
                    len(serialized) / (1024.0 * 1024.0)
                ),
                serialization_format="pickle",
            )
        )

"""Run measurement strategies independently and assemble profile results."""

from __future__ import annotations

from typing import Any, Literal, Sequence

from modeldiet.profiling.measurements import BaseMeasurement
from modeldiet.result import (
    SCHEMA_VERSION,
    MeasurementError,
    MeasurementResult,
    MetricDefinition,
    MetricValue,
    ProfileResult,
)

_DEFINITIONS = {
    ("latency", "mean_ms"): MetricDefinition(
        "latency.mean",
        "ms",
        "Mean per-sample inference latency",
        "Single-row predict duration measured without tracemalloc",
    ),
    ("latency", "p50_ms"): MetricDefinition(
        "latency.p50",
        "ms",
        "50th percentile per-sample inference latency",
        "Single-row predict duration measured without tracemalloc",
    ),
    ("latency", "p90_ms"): MetricDefinition(
        "latency.p90",
        "ms",
        "90th percentile per-sample inference latency",
        "Single-row predict duration measured without tracemalloc",
    ),
    ("latency", "p95_ms"): MetricDefinition(
        "latency.p95",
        "ms",
        "95th percentile per-sample inference latency",
        "Single-row predict duration measured without tracemalloc",
    ),
    ("latency", "p99_ms"): MetricDefinition(
        "latency.p99",
        "ms",
        "99th percentile per-sample inference latency",
        "Single-row predict duration measured without tracemalloc",
    ),
    ("latency", "sample_count"): MetricDefinition(
        "latency.sample_count",
        "count",
        "Number of samples timed",
        "Count of samples included in the latency distribution",
    ),
    (
        "python_traced_allocation",
        "traced_peak_inference_allocation_mb",
    ): MetricDefinition(
        "python_traced.peak_allocation",
        "MiB",
        "Peak Python allocation",
        "Peak traced Python allocations during a separate inference pass; excludes untracked native allocations",
    ),
    ("process_rss", "rss_before_inference_mb"): MetricDefinition(
        "process_rss.before",
        "MiB",
        "Process RSS before inference",
        "Whole-process RSS endpoint snapshot; not model-only or peak RSS",
    ),
    ("process_rss", "rss_after_inference_mb"): MetricDefinition(
        "process_rss.after",
        "MiB",
        "Process RSS after inference",
        "Whole-process RSS endpoint snapshot; not model-only or peak RSS",
    ),
    ("process_rss", "rss_delta_mb"): MetricDefinition(
        "process_rss.delta",
        "MiB",
        "Process RSS change",
        "Difference between whole-process RSS endpoint snapshots",
    ),
    ("pickle_size", "serialized_model_size_mb"): MetricDefinition(
        "pickle.size",
        "MiB",
        "Pickle representation size",
        "Size of pickle.dumps(model) bytes; does not imply portable or safe loading",
    ),
    ("pickle_size", "serialization_format"): MetricDefinition(
        "pickle.format", "format", "Serialization format", "Python pickle format"
    ),
}


def _definition(name: str, key: str) -> MetricDefinition:
    return _DEFINITIONS.get(
        (name, key),
        MetricDefinition(
            f"{name}.{key}",
            "unspecified",
            key,
            "Custom measurement value; unit and semantics were not specified by a built-in definition",
        ),
    )


def run_measurements(
    model: Any,
    X: Any,
    measurements: Sequence[BaseMeasurement],
    *,
    on_error: Literal["raise", "record"],
) -> ProfileResult:
    names = [getattr(m, "name", m.__class__.__name__) for m in measurements]
    if len(set(names)) != len(names):
        raise ValueError("measurement names must be unique")
    results: dict[str, MeasurementResult] = {}
    for name, measurement in zip(names, measurements):
        try:
            raw = measurement.measure(model, X)
            metrics = {
                key: MetricValue(_definition(name, key), value)
                for key, value in raw.items()
            }
            results[name] = MeasurementResult(name=name, metrics=metrics)
        except Exception as exc:
            if on_error == "raise":
                raise RuntimeError(f"Measurement '{name}' failed: {exc}") from exc
            results[name] = MeasurementResult(
                name=name, error=MeasurementError(type(exc).__name__, str(exc))
            )
    shape = getattr(X, "shape", None)
    sample_count = int(shape[0]) if shape is not None else len(X)
    feature_count = (
        int(shape[1])
        if shape is not None and len(shape) > 1
        else (len(X[0]) if sample_count else None)
    )
    return ProfileResult(
        SCHEMA_VERSION,
        results,
        model.__class__.__name__,
        model.__class__.__module__,
        type(X).__name__,
        sample_count,
        feature_count,
    )

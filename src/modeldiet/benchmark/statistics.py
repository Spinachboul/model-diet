from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np


def calculate_statistics(values: Sequence[float]) -> dict[str, float]:
    """Calculate statistics across independent benchmark runs."""
    measurements = np.asarray(values, dtype=float)
    if len(measurements) == 0:
        raise ValueError("No benchmark measurements provided")

    mean = float(np.mean(measurements))
    std = float(np.std(measurements, ddof=1)) if len(measurements) > 1 else 0.0
    cv = (std / mean * 100) if mean != 0 else 0.0
    return {
        "mean": mean,
        "median": float(np.median(measurements)),
        "std_dev": std,
        "coefficient_of_variation": float(cv),
        "min": float(np.min(measurements)),
        "max": float(np.max(measurements)),
        "p90": float(np.percentile(measurements, 90)),
        "p95": float(np.percentile(measurements, 95)),
        "p99": float(np.percentile(measurements, 99)),
    }


def summarize_runs(
    runs: Sequence[Mapping[str, Any]],
) -> dict[str, dict[str, float]]:
    """Aggregate measurements from multiple independent benchmark runs."""
    metrics = [
        "training_time",
        "loading_time",
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
    ]
    legacy_names = {
        "traced_peak_inference_allocation_mb": "traced_peak_memory_usage",
        "rss_after_inference_mb": "processed_rss",
    }
    summary: dict[str, dict[str, float]] = {}
    for metric in metrics:
        legacy_name = legacy_names.get(metric)
        values = []
        for run in runs:
            if metric in run:
                values.append(run[metric])
            elif legacy_name is not None and legacy_name in run:
                values.append(run[legacy_name])
        values = [value for value in values if value is not None]
        if values:
            summary[metric] = calculate_statistics(values)
    return summary

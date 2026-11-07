"""Real user workflows that exercise Model Diet end to end."""

import json
import math
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from modeldiet import ProfileResult, profile
from modeldiet.profiling.benchmark import run_repeated_benchmark


def test_fitted_random_forest_profile_and_exports(tmp_path):
    rng = np.random.default_rng(42)
    X = rng.random((40, 5))
    y = rng.integers(0, 2, size=40)

    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    assert hasattr(model, "estimators_")

    result = profile(model=model, X=X[:8], include_environment=True)

    assert isinstance(result, ProfileResult)
    assert result.model_class == "RandomForestClassifier"
    assert result.sample_count == 8
    assert result.feature_count == 5
    assert result.environment is not None
    assert {"python_version", "platform", "numpy_version"} <= result.environment.keys()

    latency = result.measurements["latency"]
    assert latency.succeeded
    expected_identifiers = {
        "mean_ms": "latency.mean",
        "p50_ms": "latency.p50",
        "p90_ms": "latency.p90",
        "p95_ms": "latency.p95",
        "p99_ms": "latency.p99",
    }
    for key, identifier in expected_identifiers.items():
        metric = latency.metrics[key]
        assert math.isfinite(metric.value)
        assert metric.value >= 0
        assert metric.definition.identifier == identifier
        assert metric.definition.unit == "ms"
    assert latency.metrics["sample_count"].value == 8
    assert latency.metrics["sample_count"].definition.unit == "count"

    json_path = tmp_path / "profile.json"
    markdown_path = tmp_path / "profile.md"
    result.to_json(json_path)
    result.to_markdown(markdown_path)

    exported = json.loads(json_path.read_text(encoding="utf-8"))
    assert exported["model_class"] == "RandomForestClassifier"
    assert exported["sample_count"] == 8
    assert exported["feature_count"] == 5
    assert exported["environment"]
    mean_definition = exported["measurements"]["latency"]["metrics"]["mean_ms"][
        "definition"
    ]
    assert mean_definition["identifier"] == "latency.mean"

    report = markdown_path.read_text(encoding="utf-8")
    assert "RandomForestClassifier" in report
    assert "latency.mean" in report
    assert "Single-row predict duration" in report
    assert "## Environment" in report


def test_real_logistic_regression_benchmark_subprocess(tmp_path, monkeypatch):
    output_dir = tmp_path / "benchmark-output"
    monkeypatch.chdir(tmp_path)

    summary = run_repeated_benchmark("lr", repetitions=1, output_dir=output_dir)

    raw_path = output_dir / "raw_runs" / "lr_run_1.json"
    summary_path = output_dir / "summaries" / "lr_summary.json"
    assert raw_path.is_file()
    assert summary_path.is_file()

    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    exported_summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert raw["model"] == "lr"
    assert raw["training_time"] >= 0
    assert raw["loading_time"] >= 0
    for field in (
        "mean_inference_latency",
        "p99_latency",
        "traced_peak_inference_allocation_mb",
    ):
        assert math.isfinite(raw[field])
        assert raw[field] >= 0
    assert raw["measurement_details"]
    assert raw["measurement_details"]["latency"]["mean_ms"] >= 0
    assert raw["measurement_details"]["latency"]["p99_ms"] >= 0
    assert raw["environment"]
    assert "mean_inference_latency" in exported_summary
    assert exported_summary["mean_inference_latency"]["mean"] >= 0
    assert (
        summary["mean_inference_latency"]["mean"]
        == exported_summary["mean_inference_latency"]["mean"]
    )

    generated_files = {
        path.resolve() for path in output_dir.rglob("*") if path.is_file()
    }
    assert generated_files == {raw_path.resolve(), summary_path.resolve()}
    assert not (Path.cwd() / "results").exists()

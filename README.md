# Model Diet

Model Diet profiles inference characteristics of an already-fitted Python model and returns structured, exportable results.

For a detailed walkthrough, see the [application guide](docs/application.md) or the [hosted documentation source](docs/index.md).

## What is Model Diet?

Model Diet is a Python library for measuring model inference behavior on representative input data. It accepts a fitted object with a `predict(X)` method, runs one or more measurement strategies, and returns a `ProfileResult` with metric definitions and values.

## Why Model Diet?

Model Diet helps machine learning engineers inspect inference cost before integrating a model into an application. It can help answer questions such as how long single-row predictions take and how much Python-traced memory or process RSS changes during inference.

The default profile measures latency only. It does **not** evaluate model accuracy, compare predictions with labels, or determine whether a model is suitable for a task.

## Installation

The core package requires Python 3.11 or later. Install the distribution with pip:

```bash
python -m pip install modeldiet
```

The Quick Start uses scikit-learn, which is an optional demo dependency. Install it with:

```bash
python -m pip install "modeldiet[demo]"
```

## Quick Start

This example trains a small classifier, profiles its inference latency, and writes JSON and Markdown reports:

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from modeldiet import profile

rng = np.random.default_rng(42)
X = rng.random((100, 5))
y = rng.integers(0, 2, size=100)

model = RandomForestClassifier(n_estimators=20, random_state=42)
model.fit(X, y)

result = profile(model=model, X=X)
print(result.measurements["latency"].metrics["mean_ms"].value)

result.to_json("profile.json")
result.to_markdown("profile.md")
```

`profile()` calls `predict()` once per input row for each selected measurement. Pass representative inputs for the prediction workload you want to understand.

## Supported Models and Inputs

The model must be fitted and provide a callable `predict(X)` method. Model Diet does not require a particular estimator base class. Scikit-learn estimators are one example; other Python models can be used if their `predict` method accepts the supplied rows.

`X` must contain non-empty, two-dimensional tabular data in one of these forms:

- NumPy arrays
- pandas DataFrames
- Lists or tuples of rows

Rows are passed to `predict()` one at a time with a batch dimension preserved. For a DataFrame, row slices remain DataFrames. Inputs should use the same preprocessing and feature representation expected by the fitted model.

## Measurement Metrics

By default, `profile()` runs `LatencyMeasurement` only. Each input row is predicted separately, after an optional warmup prediction, and timed without `tracemalloc` enabled.

| Metric | Unit | Meaning |
| --- | --- | --- |
| `mean_ms` | ms | Mean duration of a single-row prediction. |
| `p50_ms` | ms | Median single-row prediction duration. |
| `p90_ms` | ms | 90th percentile single-row prediction duration. |
| `p95_ms` | ms | 95th percentile single-row prediction duration. |
| `p99_ms` | ms | 99th percentile single-row prediction duration. |
| `sample_count` | count | Number of input rows timed. |

Other built-in strategies are available from `modeldiet.profiling`:

| Strategy | Result fields | Interpretation |
| --- | --- | --- |
| `TracedAllocationMeasurement` | `traced_peak_inference_allocation_mb` | Peak Python allocations observed during a separate inference pass. Native allocations not tracked by `tracemalloc` are excluded. |
| `ProcessRSSMeasurement` | `rss_before_inference_mb`, `rss_after_inference_mb`, `rss_delta_mb` | Whole-process resident memory snapshots before and after a separate inference pass. These are endpoint snapshots, not peak memory or model-only memory. |
| `SerializationMeasurement` | `serialized_model_size_mb`, `serialization_format` | Size of the model's Python pickle representation. This does not imply the pickle is portable or safe to load. |

Each strategy runs in its own pass. Measurements therefore do not share a single timed execution, and results can vary with hardware, operating system, background load, Python version, and model library configuration.

## Understanding `ProfileResult`

`profile()` returns a `ProfileResult` with:

- `schema_version`: result schema version.
- `measurements`: mapping of strategy names to `MeasurementResult` objects. Successful results contain metrics; failures recorded with `on_error="record"` contain an error.
- `model_class` and `model_module`: model type metadata.
- `input_type`, `sample_count`, and `feature_count`: metadata about the profiling input.
- `environment`: optional Python, platform, CPU, RAM, and selected library metadata.

For example, read the default latency mean with:

```python
mean_latency_ms = result.measurements["latency"].metrics["mean_ms"].value
```

Each metric is a `MetricValue` with a numeric `value` and a `definition` containing its identifier, unit, description, and semantics. When a measurement raises an exception, the default `on_error="raise"` raises a `RuntimeError`. Set `on_error="record"` to retain the error in the result and continue with other strategies.

## Exporting Results

Write a versioned JSON structure or a human-readable Markdown report:

```python
result.to_json("profile.json")
result.to_markdown("profile.md")
```

Both methods accept a string or `pathlib.Path`. The parent directory must exist. Non-finite floating-point values in JSON are written as `null`.

## Advanced Usage

Select additional built-in measurements and include environment metadata:

```python
from modeldiet import profile
from modeldiet.profiling import (
    ProcessRSSMeasurement,
    SerializationMeasurement,
    TracedAllocationMeasurement,
)

result = profile(
    model=model,
    X=X,
    measurements=[
        TracedAllocationMeasurement(),
        ProcessRSSMeasurement(),
        SerializationMeasurement(),
    ],
    include_environment=True,
)
```

Latency is not included automatically when you provide `measurements`; include `LatencyMeasurement()` explicitly if you want latency alongside other strategies. Measurement names must be unique. Custom strategies can subclass `BaseMeasurement` and implement `measure(model, X=None)`; custom metric units and semantics are not inferred by Model Diet.

## Limitations

- The API expects an already-fitted model with `predict()` and tabular input. It does not train models or assess prediction quality.
- Latency is measured for individual rows, not batches, concurrent requests, or end-to-end application requests.
- Memory figures describe Python-traced allocations or whole-process RSS; the package does not currently report GPU memory or peak RSS during inference.
- Timing depends on the local machine, software stack, and workload. Use consistent conditions when comparing results.
- Model Diet does not currently provide built-in adapters for PyTorch, TensorFlow, or ONNX Runtime. A compatible `predict()` method is required.

## Contributing

Contributions and issue reports are welcome. For code changes, install the project with its test and demo dependencies and run the test suite:

```bash
python -m pip install -e ".[test,demo]"
python -m pytest -v
```

Please keep changes focused and include tests for changed behavior.

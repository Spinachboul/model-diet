# API reference

## `modeldiet.profile`

```python
profile(
    model,
    X,
    *,
    measurements=None,
    on_error="raise",
    include_environment=False,
)
```

Profile a fitted model and return a `ProfileResult`.

| Argument | Description |
| --- | --- |
| `model` | Fitted object with a callable `predict(X)` method. |
| `X` | Non-empty, two-dimensional NumPy array, pandas DataFrame, list of rows, or tuple of rows. |
| `measurements` | Optional sequence of `BaseMeasurement` instances. If omitted, only `LatencyMeasurement()` is used. Passing a sequence replaces the default; add latency explicitly if desired. Names must be unique. |
| `on_error` | `"raise"` (default) raises `RuntimeError` on measurement failure. `"record"` stores the failure and continues with remaining measurements. |
| `include_environment` | If true, attaches collected host, Python, and selected library metadata. |

Invalid `on_error`, a model without `predict()`, missing input, empty measurements, and non-`BaseMeasurement` strategies raise errors before or during profiling.

## Built-in measurements

Import strategies from `modeldiet.profiling`:

```python
from modeldiet.profiling import (
    BaseMeasurement,
    LatencyMeasurement,
    ProcessRSSMeasurement,
    SerializationMeasurement,
    TracedAllocationMeasurement,
)
```

`LatencyMeasurement(warmup_iterations=1)` accepts a non-negative number of warmup predictions. Other built-in strategies currently use their default behavior and accept no constructor options.

## `ProfileResult`

Import from `modeldiet`:

```python
from modeldiet import ProfileResult
```

The result exposes `schema_version`, `measurements`, `model_class`, `model_module`, `input_type`, `sample_count`, `feature_count`, and optional `environment` attributes. Each measurement entry is a `MeasurementResult` with a `name`, a `metrics` mapping, and an optional `error`. Its `succeeded` property is true when there is no error.

Each metric value is a `MetricValue`; read its payload from `.value` and its `MetricDefinition` from `.definition`. The definition includes `identifier`, `unit`, `description`, and `semantics`.

## Export methods

```python
result.to_json(path)
result.to_markdown(path)
```

`path` is a string or `pathlib.Path`. The parent directory must already exist. JSON is indented, ends with a newline, and uses `null` for non-finite float values. Markdown renders measurement metrics and optional environment metadata.

## Custom measurements

Subclass `BaseMeasurement`, set a unique strategy `name`, and implement `measure(model, X=None)` to return a mapping of serializable keys and values. Built-in metric definitions are provided for built-in strategies. Custom values receive generic definitions; Model Diet cannot infer their units or semantics.

# Measurements and interpretation

Each built-in measurement runs its own prediction pass. The default profile contains latency only. Additional measurements run only when explicitly selected.

## Latency

`LatencyMeasurement` performs an optional warmup (one prediction by default), then calls `predict()` for each row as a batch of one. It uses `time.perf_counter()` and does not enable `tracemalloc` during timing.

| Field | Unit | Meaning |
| --- | --- | --- |
| `mean_ms` | ms | Arithmetic mean of single-row prediction durations. |
| `p50_ms` | ms | 50th percentile (median) duration. |
| `p90_ms` | ms | 90th percentile duration. |
| `p95_ms` | ms | 95th percentile duration. |
| `p99_ms` | ms | 99th percentile duration. |
| `sample_count` | count | Number of rows timed; does not include warmup predictions. |

These measurements describe the supplied sample and environment. They are not latency guarantees and do not include data loading, preprocessing outside `predict()`, network time, or application overhead.

## Python traced allocation

`TracedAllocationMeasurement` calls `predict()` for each row with Python `tracemalloc` active and reports `traced_peak_inference_allocation_mb` in MiB. It is a separate pass from latency. It excludes allocations in native code that Python's tracing does not observe, so it is not total memory consumption.

## Process resident memory

`ProcessRSSMeasurement` reports `rss_before_inference_mb`, `rss_after_inference_mb`, and `rss_delta_mb`, in MiB. These are process-wide resident set size snapshots around a separate inference pass. They include the Python process and its other loaded data, are not model-only values, and do not capture peak RSS during the pass. The delta can be negative if the process releases memory.

## Pickle representation size

`SerializationMeasurement` serializes the Python model object with `pickle.dumps()` and reports `serialized_model_size_mb` and `serialization_format`. This is a measurement of the in-memory pickle byte representation, not necessarily the model's normal saved artifact size. Python pickle can execute code when loading; do not load untrusted pickle files.

## Environment metadata

Pass `include_environment=True` to collect Python and platform details, CPU counts and frequency, installed NumPy, scikit-learn, and XGBoost versions, RAM, and common thread-related environment variables. This is descriptive context, not a guarantee that two runs are comparable.

## Comparing runs

For a meaningful comparison:

- Use the same representative input rows and preprocessing.
- Keep model configuration, library versions, hardware, and thread settings consistent.
- Run under similar system load and repeat profiles if timing stability matters.
- Compare the same metric with its unit and semantics; do not treat RSS delta as peak memory or per-row latency as throughput.

# Changelog

This changelog records user-visible changes to Model Diet. Version 0.1.0 is the initial release candidate and has not been marked as published here.

## [0.1.0] - Unreleased

### Added

- `modeldiet.profile()` for profiling a fitted model that implements `predict(X)`.
- Single-row inference latency by default, with percentile metrics and explicit metric definitions.
- Optional measurements for Python-traced allocations, process RSS snapshots, and pickle representation size.
- Structured `ProfileResult` objects with JSON and Markdown export.
- Optional runtime environment metadata and a configurable error-recording mode.
- Python package metadata and CI coverage for the supported Python versions.

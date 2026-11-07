"""Compatibility import for repeated benchmark orchestration."""

# Retained so callers that patch this shared module can continue to do so.

from modeldiet.benchmark.runner import run_repeated_benchmark

__all__ = ["run_repeated_benchmark"]

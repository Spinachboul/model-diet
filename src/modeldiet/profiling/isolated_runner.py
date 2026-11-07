"""Compatibility imports and CLI delegate for the benchmark worker."""

from modeldiet.benchmark.worker import create_model, load_dataset, main, run_model

__all__ = ["create_model", "load_dataset", "run_model", "main"]


if __name__ == "__main__":
    main()

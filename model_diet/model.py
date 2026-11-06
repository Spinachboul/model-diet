import pickle
import time
import tracemalloc
from typing import Any

import numpy as np
import psutil  # type: ignore


class Model:

    def __init__(
        self,
        loading_time: float = 0.0,
        mean_inference_latency: float = 0.0,
        p50_latency: float = 0.0,
        p90_latency: float = 0.0,
        p95_latency: float = 0.0,
        p99_latency: float = 0.0,
        traced_peak_memory_usage: float = 0.0,
        processed_rss: float = 0.0,
        serialized_model_size: float = 0.0,
    ):

        self.loading_time = loading_time

        self.mean_inference_latency = mean_inference_latency
        self.p50_latency = p50_latency
        self.p90_latency = p90_latency
        self.p95_latency = p95_latency
        self.p99_latency = p99_latency

        self.traced_peak_memory_usage = traced_peak_memory_usage
        self.processed_rss = processed_rss
        self.serialized_model_size = serialized_model_size

        self.clf: Any = None

    def profile_execution(self, X_test: Any, load_start_time=None):
        """
        Profile inference latency, memory usage
        and serialized model footprint.
        """

        # ---------------------------------
        # 1. Loading time
        # ---------------------------------

        if load_start_time is not None:

            self.loading_time = time.perf_counter() - load_start_time

        # ---------------------------------
        # 2. Prepare input
        # ---------------------------------

        samples = X_test.to_numpy() if hasattr(X_test, "to_numpy") else X_test

        # ---------------------------------
        # 3. Warm-up
        # ---------------------------------

        if len(samples) > 0:

            warmup_sample = samples[0].reshape(1, -1)

            self.clf.predict(warmup_sample)

        # ---------------------------------
        # 4. Inference profiling
        # ---------------------------------

        latencies = []

        tracemalloc.start()

        try:

            for sample in samples:

                sample_input = sample.reshape(1, -1)

                start_time = time.perf_counter()

                self.clf.predict(sample_input)

                end_time = time.perf_counter()

                latencies.append((end_time - start_time) * 1000)

            current_mem, peak_mem = tracemalloc.get_traced_memory()

        finally:

            tracemalloc.stop()

        # ---------------------------------
        # 5. Latency statistics
        # ---------------------------------

        latencies = np.asarray(latencies)

        if len(latencies) == 0:
            raise ValueError("Test dataset is empty")

        self.mean_inference_latency = float(np.mean(latencies))

        self.p50_latency = float(np.percentile(latencies, 50))

        self.p90_latency = float(np.percentile(latencies, 90))

        self.p95_latency = float(np.percentile(latencies, 95))

        self.p99_latency = float(np.percentile(latencies, 99))

        # ---------------------------------
        # 6. Memory profiling
        # ---------------------------------

        self.traced_peak_memory_usage = float(peak_mem / (1024 * 1024))

        process = psutil.Process()

        self.processed_rss = float(process.memory_info().rss / (1024 * 1024))

        # ---------------------------------
        # 7. Serialized model size
        # ---------------------------------

        serialized_data = pickle.dumps(self.clf)

        self.serialized_model_size = float(len(serialized_data) / (1024 * 1024))

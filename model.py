import time
import tracemalloc
import psutil
import pickle
import numpy as np
from typing import Any

class Model:
    def __init__(self, 
                loading_time: float=0.0, 
                mean_inference_latency: float=0.0, 
                p50_latency: float=0.0, 
                p90_latency: float=0.0, 
                p95_latency: float=0.0, 
                p99_latency: float=0.0, 
                traced_peak_memory_usage: float=0.0, 
                processed_rss: float=0.0, 
                serialized_model_size: float=0.0):
        self.loading_time = loading_time
        self.mean_inference_latency = mean_inference_latency
        self.p50_latency = p50_latency
        self.p90_latency = p90_latency
        self.p95_latency = p95_latency
        self.p99_latency = p99_latency
        self.traced_peak_memory_usage = traced_peak_memory_usage
        self.processed_rss = processed_rss
        self.serialized_model_size = serialized_model_size


    def profile_execution(self,
                          X_test: Any,
                          load_start_time: float):
        """Runs inference row by row (or in batches) to capture latencies,
        while tracing peak memory usage and calculating model footprint.
        """

        # compute load time
        if load_start_time is not None:
            self.loading_time = time.time() - load_start_time

        # trace memory and run inference
        tracemalloc.start()
        latencies = []

        # we loop through samples to get multiple
        # runs for precise percentile metrics
        
        samples = X_test.to_numpy() if hasattr(X_test, "to_numpy") else X_test

        for sample in samples:
            sample_input = sample.reshape(1, -1)
            start_time = time.perf_counter()
            # this is assigned in the child wrappers
            self.clf.predict(sample_input)
            end_time = time.perf_counter()
            latencies.append(end_time - start_time)

        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # convert latencies into ms
        latencies_ms = np.array(latencies) * 1000

        # compute latency metrics
        self.mean_inference_latency = float(np.mean(latencies_ms))
        self.p50_latency = float(np.percentile(latencies_ms, 50))
        self.p90_latency = float(np.percentile(latencies_ms, 90))
        self.p95_latency = float(np.percentile(latencies_ms, 95))
        self.p99_latency = float(np.percentile(latencies_ms, 99))

        # compute memory and size metrics
        self.traced_peak_memory_usage = float(peak_mem / (1024 * 1024))  # Convert to MB

        # full resident set is the total memory used by the process, including all shared libraries and memory-mapped files
        process = psutil.Process()
        self.processed_rss = float(process.memory_info().rss / (1024 * 1024))  # Convert to MB

        # serialized model size via pickle payload size
        self.serialized_model_size = len(pickle.dumps(self.clf)) / (1024 * 1024)  # Convert to MB
        


        

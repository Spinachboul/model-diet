from sklearn.metrics import accuracy_score, classification_report
import numpy as np

class Report:
    def __init__(self, model, X_test, y_test):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test

    def print_report(self):
        # Generate predictions to include standard ML metrics alongside telemetry
        y_pred = self.model.clf.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        
        # Extract model class name dynamically
        model_name = self.model.__class__.__name__

        print("=" * 60)
        print(f" BENCHMARK REPORT: {model_name.upper()} ".center(60, "="))
        print("=" * 60)
        
        # 1. Model & General Performance Metadata
        print("\n [1] MODEL METADATA & ACCURACY")
        print(f" • Model Architecture      : {model_name}")
        print(f" • Model Loading Time       : {self.model.loading_time:.4f} sec")
        print(f" • Test Dataset Accuracy    : {accuracy * 100:.2f}%")
        
        # 2. Performance and Latency Statistics
        print("\n [2] INFERENCE LATENCY PROFILE")
        print(f" • Mean Inference Latency  : {self.model.mean_inference_latency:.4f} ms")
        print(f" • p50 Latency (Median)     : {self.model.p50_latency:.4f} ms")
        print(f" • p90 Latency              : {self.model.p90_latency:.4f} ms")
        print(f" • p95 Latency              : {self.model.p95_latency:.4f} ms")
        print(f" • p99 Latency (Tail)       : {self.model.p99_latency:.4f} ms")
        
        # 3. Hardware Profile and Sizes
        print("\n [3] MEMORY & STORAGE FOOTPRINT PROFILE")
        print(f" • Traced Peak Memory Usage : {self.model.traced_peak_memory_usage:.2f} MB")
        print(f" • Process RSS Memory       : {self.model.processed_rss:.2f} MB")
        print(f" • Serialized Model Size    : {self.model.serialized_model_size:.4f} MB")
        
        print("\n" + "=" * 60 + "\n")

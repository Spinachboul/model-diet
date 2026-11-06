from sklearn.metrics import accuracy_score


class Report:
    def __init__(self, model, X_test, y_test):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test

    def print_report(self):
        y_pred = self.model.clf.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        model_name = self.model.__class__.__name__

        print("=" * 60)
        print(f" BENCHMARK REPORT: {model_name.upper()} ".center(60, "="))
        print("=" * 60)
        print("\n [1] MODEL METADATA & ACCURACY")
        print(f" • Model Architecture       : {model_name}")
        print(f" • Model Deserialization    : {self.model.loading_time:.4f} sec")
        print(f" • Test Dataset Accuracy    : {accuracy * 100:.2f}%")

        print("\n [2] INFERENCE LATENCY PROFILE")
        print(
            f" • Mean Inference Latency   : {self.model.mean_inference_latency:.4f} ms"
        )
        print(f" • P50 Latency              : {self.model.p50_latency:.4f} ms")
        print(f" • P90 Latency              : {self.model.p90_latency:.4f} ms")
        print(f" • P95 Latency              : {self.model.p95_latency:.4f} ms")
        print(f" • P99 Latency              : {self.model.p99_latency:.4f} ms")

        print("\n [3] MEMORY & STORAGE FOOTPRINT PROFILE")
        print(
            " • Traced Peak Inference Allocation: "
            f"{self.model.traced_peak_inference_allocation_mb:.2f} MB"
        )
        print(
            " • Process RSS Before / After     : "
            f"{self.model.rss_before_inference_mb:.2f} / "
            f"{self.model.rss_after_inference_mb:.2f} MB"
        )
        print(f" • Process RSS Delta               : {self.model.rss_delta_mb:.4f} MB")
        print(
            f" • Pickle Serialized Model Size   : {self.model.serialized_model_size:.4f} MB"
        )
        print("\n" + "=" * 60 + "\n")

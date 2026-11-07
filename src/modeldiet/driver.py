import warnings

from modeldiet.benchmark import run_repeated_benchmark


def main():
    warnings.warn(
        "modeldiet.driver.main is deprecated. Call "
        "modeldiet.benchmark.run_repeated_benchmark() once per selected model. "
        "The driver will remain available through the 0.x series and will not "
        "be removed before 1.0.0.",
        DeprecationWarning,
        stacklevel=2,
    )

    models = ["lr", "rf", "xgb"]

    repetitions = 10

    all_results = {}

    for model_name in models:

        summary = run_repeated_benchmark(model_name=model_name, repetitions=repetitions)

        all_results[model_name] = summary

    print("\n" + "=" * 60)
    print("ALL BENCHMARKS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()

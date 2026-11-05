
from profiling.benchmark import run_repeated_benchmark


def main():

    models = ["lr", "rf", "xgb"]

    repetitions = 10

    all_results = {}

    for model_name in models:

        summary = run_repeated_benchmark(
            model_name=model_name,
            repetitions=repetitions
        )

        all_results[model_name] = summary

    print("\n" + "=" * 60)
    print("ALL BENCHMARKS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()

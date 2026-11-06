import json
import subprocess
import sys
from pathlib import Path

from model_diet.profiling.statistics import summarize_runs

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULT_DIR = PROJECT_ROOT / "results"
RAW_DIR = RESULT_DIR / "raw_runs"
SUMMARY_DIR = RESULT_DIR / "summaries"


def run_repeated_benchmark(model_name, repetitions=10):

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    runs = []

    print("\n" + "=" * 60)
    print(f"REPEATED BENCHMARK: {model_name.upper()}")
    print("=" * 60)

    for iteration in range(1, repetitions + 1):

        print(
            f"\nRunning {model_name.upper()} " f"- Iteration {iteration}/{repetitions}"
        )

        output_file = RAW_DIR / (f"{model_name}_run_{iteration}.json")

        command = [
            sys.executable,
            str(PROJECT_ROOT / "profiling" / "isolated_runner.py"),
            "--model",
            model_name,
            "--output",
            str(output_file),
        ]

        result = subprocess.run(
            command, cwd=PROJECT_ROOT, capture_output=True, text=True
        )

        if result.returncode != 0:
            print("Run failed!")
            print(result.stderr)
            continue

        print(result.stdout)

        with open(output_file, "r") as file:
            run_data = json.load(file)

        runs.append(run_data)

    if not runs:
        raise RuntimeError(f"All benchmark runs failed for {model_name}")

    summary = summarize_runs(runs)

    summary_file = SUMMARY_DIR / f"{model_name}_summary.json"

    with open(summary_file, "w") as file:
        json.dump(summary, file, indent=4)

    print("\nSTATISTICAL SUMMARY")
    print("=" * 60)

    for metric, stats in summary.items():

        print(f"\n{metric}")

        print(f"Mean : {stats['mean']:.4f}")
        print(f"Std  : {stats['std_dev']:.4f}")
        print(f"CV   : {stats['coefficient_of_variation']:.2f}%")
        print(f"P95  : {stats['p95']:.4f}")

    print("\nSaved:", summary_file)

    return summary

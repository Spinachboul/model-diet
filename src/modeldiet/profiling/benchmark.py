import json
import subprocess
import sys
from pathlib import Path

from modeldiet.profiling.statistics import summarize_runs


def run_repeated_benchmark(model_name, repetitions=10, output_dir=None):
    """Run repeated benchmarks, writing results under output_dir or ./results."""
    if repetitions < 1:
        raise ValueError("repetitions must be at least one")

    result_dir = Path(output_dir) if output_dir is not None else Path.cwd() / "results"
    raw_dir = result_dir / "raw_runs"
    summary_dir = result_dir / "summaries"
    raw_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)
    runs = []

    print("\n" + "=" * 60)
    print(f"REPEATED BENCHMARK: {model_name.upper()}")
    print("=" * 60)

    for iteration in range(1, repetitions + 1):
        print(
            f"\nRunning {model_name.upper()} " f"- Iteration {iteration}/{repetitions}"
        )
        output_file = raw_dir / f"{model_name}_run_{iteration}.json"
        command = [
            sys.executable,
            "-m",
            "modeldiet.profiling.isolated_runner",
            "--model",
            model_name,
            "--output",
            str(output_file),
        ]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print("Run failed!")
            print(result.stderr)
            continue

        print(result.stdout)
        with open(output_file, "r") as file:
            runs.append(json.load(file))

    if not runs:
        raise RuntimeError(f"All benchmark runs failed for {model_name}")

    summary = summarize_runs(runs)
    summary_file = summary_dir / f"{model_name}_summary.json"
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

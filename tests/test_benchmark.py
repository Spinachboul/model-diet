import json
from pathlib import Path
from subprocess import CompletedProcess

from modeldiet.profiling import benchmark


def _successful_benchmark_run(command, **kwargs):
    output_path = Path(command[command.index("--output") + 1])
    output_path.write_text(json.dumps({"training_time": 1.0}))
    return CompletedProcess(command, 0, stdout="run complete", stderr="")


def test_repeated_benchmark_uses_configured_output_directory(tmp_path, monkeypatch):
    output_dir = tmp_path / "benchmark-results"
    monkeypatch.setattr(benchmark.subprocess, "run", _successful_benchmark_run)

    benchmark.run_repeated_benchmark("lr", repetitions=1, output_dir=output_dir)

    assert (output_dir / "raw_runs" / "lr_run_1.json").is_file()
    assert (output_dir / "summaries" / "lr_summary.json").is_file()


def test_repeated_benchmark_defaults_to_working_directory_results(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(benchmark.subprocess, "run", _successful_benchmark_run)

    benchmark.run_repeated_benchmark("lr", repetitions=1)

    assert (tmp_path / "results" / "raw_runs" / "lr_run_1.json").is_file()
    assert (tmp_path / "results" / "summaries" / "lr_summary.json").is_file()

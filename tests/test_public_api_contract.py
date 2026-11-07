import os
import subprocess
import sys
import textwrap


def test_supported_root_imports_and_public_names():
    import modeldiet
    from modeldiet import ProfileResult, profile

    assert callable(profile)
    assert ProfileResult is modeldiet.ProfileResult
    assert modeldiet.__all__ == ["profile", "ProfileResult"]


def test_supported_measurement_imports_and_public_names():
    import modeldiet.profiling as profiling
    from modeldiet.profiling import (
        BaseMeasurement,
        LatencyMeasurement,
        ProcessRSSMeasurement,
        SerializationMeasurement,
        TracedAllocationMeasurement,
    )

    assert profiling.__all__ == [
        "BaseMeasurement",
        "LatencyMeasurement",
        "ProcessRSSMeasurement",
        "SerializationMeasurement",
        "TracedAllocationMeasurement",
    ]
    assert all(
        isinstance(measurement(), BaseMeasurement)
        for measurement in (
            LatencyMeasurement,
            ProcessRSSMeasurement,
            SerializationMeasurement,
            TracedAllocationMeasurement,
        )
    )


def test_supported_result_record_imports():
    from modeldiet.result import (
        MeasurementError,
        MeasurementResult,
        MetricDefinition,
        MetricValue,
        ProfileResult,
    )

    assert all(
        isinstance(record, type)
        for record in (
            MetricDefinition,
            MetricValue,
            MeasurementError,
            MeasurementResult,
            ProfileResult,
        )
    )


def test_optional_benchmark_import_path():
    from modeldiet.profiling.benchmark import run_repeated_benchmark

    assert callable(run_repeated_benchmark)


def test_ordinary_import_has_no_optional_ml_dependencies(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            textwrap.dedent(
                """
                import sys
                import modeldiet

                assert callable(modeldiet.profile)
                assert "sklearn" not in sys.modules
                assert "xgboost" not in sys.modules
                """
            ),
        ],
        cwd=tmp_path,
        env=os.environ.copy(),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"

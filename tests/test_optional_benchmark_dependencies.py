import os
import subprocess
import sys
import textwrap

import pytest


def _run_isolated(code, tmp_path):
    result = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)],
        cwd=tmp_path,
        env=os.environ.copy(),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"


def test_importing_modeldiet_does_not_import_optional_ml_libraries(tmp_path):
    _run_isolated(
        """
        import sys
        import modeldiet

        assert callable(modeldiet.profile)
        assert "sklearn" not in sys.modules
        assert "xgboost" not in sys.modules
        """,
        tmp_path,
    )


def test_importing_isolated_runner_does_not_import_xgboost(tmp_path):
    _run_isolated(
        """
        import sys
        import modeldiet.profiling.isolated_runner

        assert "xgboost" not in sys.modules
        """,
        tmp_path,
    )


def test_new_benchmark_package_and_runner_do_not_import_optional_libraries(tmp_path):
    _run_isolated(
        """
        import sys
        import modeldiet.benchmark
        import modeldiet.benchmark.runner

        assert callable(modeldiet.benchmark.run_repeated_benchmark)
        assert "sklearn" not in sys.modules
        assert "xgboost" not in sys.modules
        """,
        tmp_path,
    )


@pytest.mark.parametrize("model_name", ["lr", "rf"])
def test_non_xgboost_benchmark_does_not_attempt_xgboost_import(model_name, tmp_path):
    other_model = "rf" if model_name == "lr" else "lr"
    _run_isolated(
        f"""
        import importlib.abc
        import sys

        class RejectXGBoost(importlib.abc.MetaPathFinder):
            def find_spec(self, fullname, path=None, target=None):
                if fullname == "xgboost" or fullname.startswith("xgboost."):
                    raise AssertionError("unexpected XGBoost import: " + fullname)

        sys.meta_path.insert(0, RejectXGBoost())
        from modeldiet.benchmark.worker import create_model

        model = create_model({model_name!r})
        assert model.clf is not None
        assert "modeldiet.benchmark.models.{model_name}" in sys.modules
        assert "modeldiet.benchmark.models.{other_model}" not in sys.modules
        assert "modeldiet.benchmark.models.xgb" not in sys.modules
        """,
        tmp_path,
    )


def test_xgboost_model_creation_when_dependency_is_installed():
    pytest.importorskip("xgboost")

    from modeldiet.benchmark.worker import create_model

    model = create_model("xgb")
    assert model.clf.__class__.__name__ == "XGBClassifier"


def test_missing_xgboost_has_install_guidance_and_preserves_cause(tmp_path):
    _run_isolated(
        """
        import importlib.abc
        import sys

        class MissingXGBoost(importlib.abc.MetaPathFinder):
            def find_spec(self, fullname, path=None, target=None):
                if fullname == "xgboost":
                    raise ModuleNotFoundError("No module named 'xgboost'", name="xgboost")

        sys.meta_path.insert(0, MissingXGBoost())
        from modeldiet.benchmark.worker import create_model

        try:
            create_model("xgb")
        except ImportError as error:
            assert "modeldiet[benchmark-xgboost]" in str(error)
            assert isinstance(error.__cause__, ModuleNotFoundError)
            assert error.__cause__.name == "xgboost"
        else:
            raise AssertionError("Expected actionable ImportError")
        """,
        tmp_path,
    )


def test_unrelated_xgboost_import_error_is_not_rewritten(tmp_path):
    _run_isolated(
        """
        import importlib.abc
        import sys

        class BrokenXGBoost(importlib.abc.MetaPathFinder):
            def find_spec(self, fullname, path=None, target=None):
                if fullname == "xgboost":
                    raise ImportError("broken XGBoost installation")

        sys.meta_path.insert(0, BrokenXGBoost())
        from modeldiet.benchmark.worker import create_model

        try:
            create_model("xgb")
        except ImportError as error:
            assert str(error) == "broken XGBoost installation"
            assert "benchmark-xgboost" not in str(error)
        else:
            raise AssertionError("Expected original ImportError")
        """,
        tmp_path,
    )


def test_unsupported_model_name_still_raises_value_error():
    from modeldiet.benchmark.worker import create_model

    with pytest.raises(ValueError, match="Unsupported model: unsupported"):
        create_model("unsupported")

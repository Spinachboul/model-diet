import json
import subprocess
import sys

import numpy as np
import pytest

from model_diet import ProfileResult, profile
from model_diet.profiling.measurements import BaseMeasurement, LatencyMeasurement


class EchoModel:
    def __init__(self):
        self.seen = []

    def predict(self, X):
        self.seen.append(X)
        return [0] * len(X)


class CustomMeasurement(BaseMeasurement):
    name = "custom"

    def measure(self, model, X=None):
        return {"score": 2.0}


class FailingMeasurement(BaseMeasurement):
    name = "failure"

    def measure(self, model, X=None):
        raise ValueError("broken")


def test_public_default_and_result_metadata():
    model = EchoModel()
    result = profile(model, np.ones((3, 2)))
    assert isinstance(result, ProfileResult)
    assert list(result.measurements) == ["latency"]
    assert result.measurements["latency"].metrics["mean_ms"].definition.unit == "ms"


@pytest.mark.parametrize("X", [np.ones((3, 2)), [[1, 2], [3, 4], [5, 6]]])
def test_supported_input_is_passed_as_slices(X):
    model = EchoModel()
    profile(model, X)
    assert all(type(item) is type(X) for item in model.seen)


def test_dataframe_input_is_preserved_when_pandas_available():
    pd = pytest.importorskip("pandas")
    X = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    model = EchoModel()
    profile(model, X)
    assert all(isinstance(item, pd.DataFrame) for item in model.seen)


def test_custom_strategy_and_duplicate_names():
    assert (
        profile(EchoModel(), [[1, 2]], measurements=[CustomMeasurement()])
        .measurements["custom"]
        .metrics["score"]
        .value
        == 2.0
    )
    with pytest.raises(ValueError, match="unique"):
        profile(
            EchoModel(),
            [[1, 2]],
            measurements=[CustomMeasurement(), CustomMeasurement()],
        )


def test_error_policies():
    with pytest.raises(RuntimeError, match="failure"):
        profile(EchoModel(), [[1, 2]], measurements=[FailingMeasurement()])
    result = profile(
        EchoModel(), [[1, 2]], measurements=[FailingMeasurement()], on_error="record"
    )
    assert result.measurements["failure"].error.message == "broken"


def test_exports_and_optional_dependency_isolation(tmp_path):
    result = profile(EchoModel(), [[1, 2]])
    json_path, md_path = tmp_path / "profile.json", tmp_path / "profile.md"
    result.to_json(json_path)
    result.to_markdown(md_path)
    assert json.loads(json_path.read_text())["schema_version"] == 1
    assert "latency.mean" in md_path.read_text()
    check = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import model_diet; assert 'sklearn' not in sys.modules; assert 'xgboost' not in sys.modules",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert check.returncode == 0, check.stderr


def test_only_latency_is_default():
    assert isinstance(LatencyMeasurement(), BaseMeasurement)

from types import SimpleNamespace

import pytest


def test_legacy_estimator_wrappers_warn_when_instantiated():
    from modeldiet.models.lr import LogisticRegressionModel
    from modeldiet.models.rf import RandomForestModel
    from modeldiet.models.xgb import XGBoostModel

    for wrapper in (LogisticRegressionModel, RandomForestModel, XGBoostModel):
        with pytest.warns(
            DeprecationWarning, match="deprecated benchmark compatibility"
        ):
            wrapper()


def test_report_warns_when_instantiated():
    from modeldiet.report import Report

    with pytest.warns(DeprecationWarning, match="Report is a deprecated"):
        Report(SimpleNamespace(), [], [])


def test_driver_warns_when_called(monkeypatch):
    from modeldiet import driver

    calls = []
    monkeypatch.setattr(
        driver,
        "run_repeated_benchmark",
        lambda model_name, repetitions: calls.append((model_name, repetitions)) or {},
    )
    with pytest.warns(DeprecationWarning, match="modeldiet.driver.main is deprecated"):
        driver.main()

    assert calls == [("lr", 10), ("rf", 10), ("xgb", 10)]

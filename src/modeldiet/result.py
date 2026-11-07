"""Structured, serializable results from a Model Diet profile."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


@dataclass(frozen=True)
class MetricDefinition:
    identifier: str
    unit: str
    description: str
    semantics: str


@dataclass(frozen=True)
class MetricValue:
    definition: MetricDefinition
    value: int | float | str | bool | None


@dataclass(frozen=True)
class MeasurementError:
    exception_type: str
    message: str


@dataclass(frozen=True)
class MeasurementResult:
    name: str
    metrics: Mapping[str, MetricValue] = field(default_factory=dict)
    error: MeasurementError | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class ProfileResult:
    schema_version: int
    measurements: Mapping[str, MeasurementResult]
    model_class: str
    model_module: str
    input_type: str
    sample_count: int | None
    feature_count: int | None
    environment: Mapping[str, Any] | None = None

    def _json_value(self) -> dict[str, Any]:
        def clean(value: Any) -> Any:
            if isinstance(value, float) and not math.isfinite(value):
                return None
            if isinstance(value, dict):
                return {key: clean(item) for key, item in value.items()}
            if isinstance(value, (list, tuple)):
                return [clean(item) for item in value]
            return value

        return clean(asdict(self))

    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(self._json_value(), indent=2, allow_nan=False) + "\n",
            encoding="utf-8",
        )

    def to_markdown(self, path: str | Path) -> None:
        lines = [
            "# Model Diet profile",
            "",
            f"- Schema version: {self.schema_version}",
            f"- Model: `{self.model_module}.{self.model_class}`",
            f"- Input: `{self.input_type}` ({self.sample_count} samples, {self.feature_count} features)",
            "",
        ]
        for name, result in self.measurements.items():
            lines.extend([f"## {name}", ""])
            if result.error:
                lines.append(
                    f"Failed: `{result.error.exception_type}`: {result.error.message}"
                )
            else:
                lines.extend(
                    [
                        "| Metric | Value | Unit | Description | Semantics |",
                        "|---|---:|---|---|---|",
                    ]
                )
                for metric in result.metrics.values():
                    definition = metric.definition
                    lines.append(
                        f"| `{definition.identifier}` | {metric.value} | {definition.unit} | {definition.description} | {definition.semantics} |"
                    )
            lines.append("")
        if self.environment is not None:
            lines.extend(
                [
                    "## Environment",
                    "",
                    "```json",
                    json.dumps(self.environment, indent=2, allow_nan=False),
                    "```",
                    "",
                ]
            )
        Path(path).write_text("\n".join(lines), encoding="utf-8")

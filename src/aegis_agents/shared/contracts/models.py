"""Shared contract models for planning and messaging."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class MessageHeaders(BaseModel):
    """Standard message headers for all transports."""

    sender: str = Field(..., description="System or service that sent the message")
    timestamp: datetime = Field(..., description="UTC timestamp when message was produced")
    correlation_id: str = Field(..., description="Correlation ID for tracing")
    message_id: str | None = Field(default=None, description="Optional message identifier")
    trace_id: str | None = Field(default=None, description="Optional trace identifier")


class TestProjectRef(BaseModel):
    """Reference to a test project."""

    id: int
    project_id: int
    name: str


class EnvironmentRef(BaseModel):
    """Reference to an environment."""

    id: int
    name: str
    base_url: str


class DomainRef(BaseModel):
    """Reference to a business domain."""

    id: int
    name: str


class AuthProfileRef(BaseModel):
    """Reference to an auth profile."""

    id: int
    name: str
    type: str


class ApiCallRef(BaseModel):
    """Reference to an API call used for supporting context."""

    id: int
    name: str
    method: str
    path: str


class ApiCallSpec(BaseModel):
    """API call specification used for planning."""

    id: int
    name: str
    method: str
    path: str
    description: str | None = None
    request_schema: dict[str, Any] | None = None
    response_schema: dict[str, Any] | None = None
    response_status_codes: list[int] | None = None
    request_examples: list[dict[str, Any] | str] | None = None
    response_examples: list[dict[str, Any] | str] | None = None


class StepPlan(BaseModel):
    """A single test step within a scenario."""

    step_number: int
    step_name: str


class ScenarioOutlineHeader(BaseModel):
    """Outline column definition."""

    name: str
    type: str | None = None


class ScenarioOutlineRow(BaseModel):
    """Outline data row."""

    data: dict[str, Any]


class ScenarioOutline(BaseModel):
    """Scenario outline configuration."""

    headers: list[ScenarioOutlineHeader]
    rows: list[ScenarioOutlineRow]


class ScenarioPlan(BaseModel):
    """Planned scenario definition."""

    scenario_number: int
    name: str
    type: str | None = None
    priority: str | None = None
    tags: list[str] | None = None
    description: str | None = None
    outlines: list[ScenarioOutline] | None = None
    steps: list[StepPlan]


class FeaturePlan(BaseModel):
    """Planned feature definition."""

    feature_number: int
    feature_name: str
    feature_tags: list[str] | None = None
    scenarios: list[ScenarioPlan]


class CoverageAnalysis(BaseModel):
    """Coverage analysis details for a plan."""

    endpoints_covered: int | None = None
    total_endpoints: int | None = None
    coverage_percentage: float | None = None
    missing_endpoints: list[str] | None = None


class PlanMetrics(BaseModel):
    """Metrics collected during planning."""

    tokens_used: int | None = None
    estimated_duration: str | None = None

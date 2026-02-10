"""Contracts for test planning events."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..models import CoverageAnalysis, FeaturePlan, PlanMetrics


class TestPlanningStartedEvent(BaseModel):
    """Event emitted when planning starts."""

    trace_id: str = Field(..., description="Trace identifier")
    specification_id: int = Field(..., description="Specification identifier")


class TestPlanningProgressEvent(BaseModel):
    """Event emitted to report planning progress."""

    trace_id: str = Field(..., description="Trace identifier")
    specification_id: int = Field(..., description="Specification identifier")
    percentage: int = Field(..., ge=0, le=100, description="Progress percentage")
    message: str | None = Field(default=None, description="Progress message")


class TestPlanningCompletedEvent(BaseModel):
    """Event emitted when planning completes."""

    trace_id: str = Field(..., description="Trace identifier")
    specification_id: int = Field(..., description="Specification identifier")
    summary: str = Field(..., description="Plan summary")
    requires_approval: bool = Field(..., description="Whether approval is required")
    features: list[FeaturePlan]
    coverage_analysis: CoverageAnalysis | None = None
    metrics: PlanMetrics | None = None


class TestPlanningFailedEvent(BaseModel):
    """Event emitted when planning fails."""

    trace_id: str = Field(..., description="Trace identifier")
    specification_id: int = Field(..., description="Specification identifier")
    error_type: str = Field(..., description="Error category")
    message: str = Field(..., description="Error message")

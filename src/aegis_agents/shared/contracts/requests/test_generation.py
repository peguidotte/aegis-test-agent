"""Contracts for test generation requests."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from ..models import (
    ApiCallRef,
    ApiCallSpec,
    AuthProfileRef,
    DomainRef,
    EnvironmentRef,
    TestProjectRef,
)


class TestGenerationRequest(BaseModel):
    """Payload for test generation request events."""

    specification_id: int = Field(..., description="Specification identifier")
    name: str = Field(..., description="Specification name")
    description: str | None = Field(default=None, description="Specification description")
    input_type: str = Field(..., description="Source input type")
    method: str = Field(..., description="Primary API method")
    path: str = Field(..., description="Primary API path")
    test_objective: str = Field(..., description="Objective of the generated tests")
    request_example: str | None = Field(default=None, description="Serialized request example")
    requires_auth: bool = Field(..., description="Whether the endpoint requires auth")
    approve_before_generation: bool = Field(
        ..., description="Whether the plan requires approval before generation"
    )
    test_project: TestProjectRef
    environment: EnvironmentRef
    domain: DomainRef | None = None
    auth_profile: AuthProfileRef | None = None
    api_call: ApiCallSpec
    supporting_api_calls: list[ApiCallRef] = Field(default_factory=list)
    trace_id: str = Field(..., description="Trace identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

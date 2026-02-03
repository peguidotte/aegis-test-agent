"""Centralized topic and queue definitions.

This module contains all messaging destinations used by agents.
Never hardcode topic names in agent code - always reference from here.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MessagingDestination:
    """Google Cloud Pub/Sub messaging destination.
    
    Attributes:
        name: Human-readable identifier for the topic.
        topic: Pub/Sub topic name.
        subscription: Pub/Sub subscription name.
    """

    name: str
    topic: str
    subscription: str


class Topics:
    """Centralized topic definitions for all agents.

    Usage:
        from aegis_agents.shared.messaging.topics import Topics

        destination = Topics.TEST_GENERATION_STARTED
        # Access topic: destination.topic
        # Access subscription: destination.subscription
    """

    # ==========================================================================
    # TEST GENERATION
    # ==========================================================================

    TEST_GENERATION_STARTED = MessagingDestination(
        name="test-generation-started",
        topic="aegis-test.test-generation.started",
        subscription="test-planner.aegis-test.test-generation.started",
    )

    # ==========================================================================
    # TEST PLANNING
    # ==========================================================================

    TEST_PLANNING_COMPLETED = MessagingDestination(
        name="test-planning-completed",
        topic="aegis-test.test-planning.completed",
        subscription="orchestrator.aegis-test.test-planning.completed",
    )

    TEST_PLANNING_FAILED = MessagingDestination(
        name="test-planning-failed",
        topic="aegis-test.test-planning.failed",
        subscription="orchestrator.aegis-test.test-planning.failed",
    )

    # ==========================================================================
    # Add more topics below as needed
    # ==========================================================================

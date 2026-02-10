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

        destination = Topics.TEST_GENERATION_REQUESTED
        # Access topic: destination.topic
        # Access subscription: destination.subscription
    """

    # ==========================================================================
    # TEST GENERATION
    # ==========================================================================

    TEST_GENERATION_REQUESTED = MessagingDestination(
        name="test-generation-requested",
        topic="aegis-test.test-generation.requested",
        subscription="test-planner.aegis-test.test-generation.requested",
    )

    # ==========================================================================
    # TEST PLANNING
    # ==========================================================================

    TEST_GENERATION_PLANNING_STARTED = MessagingDestination(
        name="test-generation-planning-started",
        topic="aegis-test.test-generation.planning.started",
        subscription="orchestrator.aegis-test.test-generation.planning.started",
    )
    
    TEST_GENERATION_PLANNED = MessagingDestination(
        name="test-generation-planning-completed",
        topic="aegis-test.test-generation.planning.completed",
        subscription="orchestrator.aegis-test.test-generation.planning.completed",
    )


    TEST_GENERATION_PLANNING_FAILED = MessagingDestination(
        name="test-generation-planning-failed",
        topic="aegis-test.test-generation.planning.failed",
        subscription="orchestrator.aegis-test.test-generation.planning.failed",
    )


    # ==========================================================================
    # Add more topics below as needed
    # ==========================================================================

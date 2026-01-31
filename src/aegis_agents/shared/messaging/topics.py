"""Centralized topic and queue definitions.

This module contains all messaging destinations used by agents.
Never hardcode topic names in agent code - always reference from here.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RabbitMQDestination:
    """RabbitMQ destination configuration."""

    queue: str
    exchange: str
    routing_key: str


@dataclass(frozen=True)
class PubSubDestination:
    """Google Cloud Pub/Sub destination configuration."""

    topic: str
    subscription: str


@dataclass(frozen=True)
class MessagingDestination:
    """Unified messaging destination for both backends."""

    name: str
    rabbitmq: RabbitMQDestination
    pubsub: PubSubDestination


class Topics:
    """Centralized topic definitions for all agents.

    Usage:
        from aegis_agents.shared.messaging.topics import Topics

        destination = Topics.TEST_GENERATION_STARTED
        # Access RabbitMQ config: destination.rabbitmq.queue
        # Access Pub/Sub config: destination.pubsub.topic
    """

    # ==========================================================================
    # TEST GENERATION
    # ==========================================================================

    TEST_GENERATION_STARTED = MessagingDestination(
        name="test-generation-started",
        rabbitmq=RabbitMQDestination(
            queue="aegis-test.test-generation.started",
            exchange="aegis-test.test-generation.exchange",
            routing_key="specification.started",
        ),
        pubsub=PubSubDestination(
            topic="aegis-test.test-generation.started",
            subscription="test-planner.aegis-test.test-generation.started",
        ),
    )

    # ==========================================================================
    # TEST PLANNING
    # ==========================================================================

    TEST_PLANNING_COMPLETED = MessagingDestination(
        name="test-planning-completed",
        rabbitmq=RabbitMQDestination(
            queue="aegis-test.test-planning.completed",
            exchange="aegis-test.test-planning.exchange",
            routing_key="planning.completed",
        ),
        pubsub=PubSubDestination(
            topic="aegis-test.test-planning.completed",
            subscription="orchestrator.aegis-test.test-planning.completed",
        ),
    )

    TEST_PLANNING_FAILED = MessagingDestination(
        name="test-planning-failed",
        rabbitmq=RabbitMQDestination(
            queue="aegis-test.test-planning.failed",
            exchange="aegis-test.test-planning.exchange",
            routing_key="planning.failed",
        ),
        pubsub=PubSubDestination(
            topic="aegis-test.test-planning.failed",
            subscription="orchestrator.aegis-test.test-planning.failed",
        ),
    )

    # ==========================================================================
    # Add more topics below as needed
    # ==========================================================================

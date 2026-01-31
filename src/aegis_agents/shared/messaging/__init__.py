"""Messaging abstractions and Pub/Sub adapters.

Usage:
    from aegis_agents.shared.messaging import (
        MessagingFactory,
        Topics,
        MessagingBackend,
    )

    # Create publisher/subscriber (backend determined by AEGIS_MESSAGING_BACKEND env var)
    publisher = MessagingFactory.create_publisher()
    subscriber = MessagingFactory.create_subscriber()

    # Publish to a topic
    await publisher.connect()
    await publisher.publish(Topics.TEST_GENERATION_STARTED, {"data": "value"})

    # Subscribe to a topic
    await subscriber.connect()
    await subscriber.subscribe(Topics.TEST_GENERATION_STARTED, my_handler)
    await subscriber.start_consuming()
"""

from .config import MessagingSettings, get_messaging_settings
from .factory import MessagingFactory
from .interfaces import MessagePublisher, MessageSubscriber
from .topics import MessagingDestination, PubSubDestination, RabbitMQDestination, Topics
from .types import MessagingBackend

__all__ = [
    "MessagingBackend",
    "MessagingDestination",
    "MessagingFactory",
    "MessagingSettings",
    "MessagePublisher",
    "MessageSubscriber",
    "PubSubDestination",
    "RabbitMQDestination",
    "Topics",
    "get_messaging_settings",
]

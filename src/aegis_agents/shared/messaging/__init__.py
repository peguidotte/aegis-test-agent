"""Messaging abstractions and Pub/Sub implementation.

Usage:
    from aegis_agents.shared.messaging import (
        PubSubPublisher,
        PubSubSubscriber,
        Topics,
    )

    # Create publisher/subscriber
    publisher = PubSubPublisher(MessagingSettings())
    subscriber = PubSubSubscriber(MessagingSettings())

    # Publish to a topic
    await publisher.connect()
    await publisher.publish(Topics.TEST_GENERATION_STARTED, {"data": "value"})

    # Subscribe to a topic
    await subscriber.connect()
    await subscriber.subscribe(Topics.TEST_GENERATION_STARTED, my_handler)
    await subscriber.start_consuming()
"""

from .config import MessagingSettings, get_messaging_settings
from .interfaces import MessagePublisher, MessageSubscriber
from .pubsub import PubSubPublisher, PubSubSubscriber
from .topics import MessagingDestination, Topics

__all__ = [
    "MessagingDestination",
    "MessagingSettings",
    "MessagePublisher",
    "MessageSubscriber",
    "PubSubPublisher",
    "PubSubSubscriber",
    "Topics",
    "get_messaging_settings",
]

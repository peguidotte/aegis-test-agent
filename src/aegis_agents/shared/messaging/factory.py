"""Factory for creating messaging clients based on configuration."""

import logging

from .backends import (
    PubSubPublisher,
    PubSubSubscriber,
    RabbitMQPublisher,
    RabbitMQSubscriber,
)
from .config import MessagingSettings, get_messaging_settings
from .interfaces import MessagePublisher, MessageSubscriber
from .types import MessagingBackend

logger = logging.getLogger(__name__)


class MessagingFactory:
    """Factory for creating messaging clients.

    Usage:
        # Using default settings from environment
        publisher = MessagingFactory.create_publisher()
        subscriber = MessagingFactory.create_subscriber()

        # Using custom settings
        settings = MessagingSettings(backend=MessagingBackend.PUBSUB)
        publisher = MessagingFactory.create_publisher(settings)
    """

    @staticmethod
    def create_publisher(settings: MessagingSettings | None = None) -> MessagePublisher:
        """Create a publisher based on configured backend.

        Args:
            settings: Optional custom settings. Uses environment if not provided.

        Returns:
            MessagePublisher implementation for the configured backend.
        """
        settings = settings or get_messaging_settings()

        logger.info(
            "Creating message publisher",
            extra={"backend": settings.backend.value},
        )

        if settings.backend == MessagingBackend.RABBITMQ:
            return RabbitMQPublisher(settings)
        elif settings.backend == MessagingBackend.PUBSUB:
            return PubSubPublisher(settings)
        else:
            raise ValueError(f"Unsupported messaging backend: {settings.backend}")

    @staticmethod
    def create_subscriber(settings: MessagingSettings | None = None) -> MessageSubscriber:
        """Create a subscriber based on configured backend.

        Args:
            settings: Optional custom settings. Uses environment if not provided.

        Returns:
            MessageSubscriber implementation for the configured backend.
        """
        settings = settings or get_messaging_settings()

        logger.info(
            "Creating message subscriber",
            extra={"backend": settings.backend.value},
        )

        if settings.backend == MessagingBackend.RABBITMQ:
            return RabbitMQSubscriber(settings)
        elif settings.backend == MessagingBackend.PUBSUB:
            return PubSubSubscriber(settings)
        else:
            raise ValueError(f"Unsupported messaging backend: {settings.backend}")

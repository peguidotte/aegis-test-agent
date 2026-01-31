"""Messaging types and enums."""

from enum import Enum


class MessagingBackend(str, Enum):
    """Supported messaging backends."""

    RABBITMQ = "rabbitmq"
    PUBSUB = "pubsub"

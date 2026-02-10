"""Abstract interfaces for messaging operations."""

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any

from .topics import MessagingDestination


class MessagePublisher(ABC):

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the messaging backend."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to the messaging backend."""

    @abstractmethod
    async def publish(
        self,
        destination: MessagingDestination,
        message: dict[str, Any],
        correlation_id: str | None = None,
    ) -> None:
        """Publish a message to the specified destination.

        Args:
            destination: The messaging destination configuration.
            message: The message payload as a dictionary.
            correlation_id: Optional correlation ID for tracing.
        """


class MessageSubscriber(ABC):
    """Abstract subscriber interface."""

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the messaging backend."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to the messaging backend."""

    @abstractmethod
    async def subscribe(
        self,
        destination: MessagingDestination,
        handler: Callable[[dict[str, Any], str | None], Awaitable[None]],
    ) -> None:
        """Subscribe to messages from the specified destination.

        Args:
            destination: The messaging destination configuration.
            handler: Async callback function that receives (message, correlation_id).
        """

    @abstractmethod
    async def start_consuming(self) -> None:
        """Start consuming messages from all subscribed destinations."""

    @abstractmethod
    async def stop_consuming(self) -> None:
        """Stop consuming messages."""

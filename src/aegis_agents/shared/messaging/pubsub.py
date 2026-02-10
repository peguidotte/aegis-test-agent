"""Google Cloud Pub/Sub messaging implementation."""

import json
import logging
import os
import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message

from .config import MessagingSettings
from .interfaces import MessagePublisher, MessageSubscriber
from .topics import MessagingDestination

logger = logging.getLogger(__name__)


class PubSubPublisher(MessagePublisher):
    """Google Cloud Pub/Sub publisher implementation."""

    def __init__(self, settings: MessagingSettings) -> None:
        self._settings = settings
        self._publisher: pubsub_v1.PublisherClient | None = None

    async def connect(self) -> None:
        self._configure_emulator()
        self._publisher = pubsub_v1.PublisherClient()
        logger.info(
            "Connected to Google Cloud Pub/Sub",
            extra={"project_id": self._settings.pubsub_project_id},
        )

    async def disconnect(self) -> None:
        if self._publisher:
            self._publisher.transport.close()
        logger.info("Disconnected from Google Cloud Pub/Sub")

    def _configure_emulator(self) -> None:
        """Configure emulator if specified."""
        if self._settings.pubsub_emulator_host:
            os.environ["PUBSUB_EMULATOR_HOST"] = self._settings.pubsub_emulator_host
            logger.info(
                "Using Pub/Sub emulator",
                extra={"host": self._settings.pubsub_emulator_host},
            )

    def _get_topic_path(self, destination: MessagingDestination) -> str:
        return f"projects/{self._settings.pubsub_project_id}/topics/{destination.topic}"

    async def publish(
        self,
        destination: MessagingDestination,
        message: dict[str, Any],
        correlation_id: str | None = None,
    ) -> None:
        if not self._publisher:
            raise RuntimeError("Publisher not connected")

        topic_path = self._get_topic_path(destination)
        data = json.dumps(message).encode("utf-8")

        attributes = {}
        if correlation_id:
            attributes["correlation_id"] = correlation_id

        future = self._publisher.publish(topic_path, data, **attributes)
        message_id = future.result()

        logger.debug(
            "Published message to Pub/Sub",
            extra={
                "topic": destination.topic,
                "message_id": message_id,
                "correlation_id": correlation_id,
            },
        )


class PubSubSubscriber(MessageSubscriber):
    """Google Cloud Pub/Sub subscriber implementation."""

    def __init__(self, settings: MessagingSettings) -> None:
        """Initialize Pub/Sub subscriber.

        Args:
            settings: Messaging configuration settings.
        """
        self._settings = settings
        self._subscriber: pubsub_v1.SubscriberClient | None = None
        self._streaming_pulls: list[Any] = []
        self._subscriptions: list[tuple[MessagingDestination, Callable]] = []

    async def connect(self) -> None:
        """Initialize Pub/Sub subscriber client."""
        self._configure_emulator()
        self._subscriber = pubsub_v1.SubscriberClient()
        logger.info(
            "Connected to Google Cloud Pub/Sub",
            extra={"project_id": self._settings.pubsub_project_id},
        )

    async def disconnect(self) -> None:
        """Close Pub/Sub subscriber client."""
        await self.stop_consuming()
        if self._subscriber:
            self._subscriber.close()
        logger.info("Disconnected from Google Cloud Pub/Sub")

    def _configure_emulator(self) -> None:
        """Configure emulator if specified."""
        if self._settings.pubsub_emulator_host:
            os.environ["PUBSUB_EMULATOR_HOST"] = self._settings.pubsub_emulator_host
            logger.info(
                "Using Pub/Sub emulator",
                extra={"host": self._settings.pubsub_emulator_host},
            )

    def _get_subscription_path(self, destination: MessagingDestination) -> str:
        """Build full subscription path."""
        return (
            f"projects/{self._settings.pubsub_project_id}"
            f"/subscriptions/{destination.subscription}"
        )

    async def subscribe(
        self,
        destination: MessagingDestination,
        handler: Callable[[dict[str, Any], str | None], Awaitable[None]],
    ) -> None:
        """Register subscription handler (actual subscription starts on start_consuming)."""
        self._subscriptions.append((destination, handler))
        logger.info(
            "Registered Pub/Sub subscription",
            extra={"subscription": destination.subscription},
        )

    async def start_consuming(self) -> None:
        """Start consuming messages from all subscribed topics."""
        if not self._subscriber:
            raise RuntimeError("Subscriber not connected")

        for destination, handler in self._subscriptions:
            subscription_path = self._get_subscription_path(destination)
            callback = self._create_message_processor(handler)

            streaming_pull = self._subscriber.subscribe(subscription_path, callback)
            self._streaming_pulls.append(streaming_pull)

            logger.info(
                "Started consuming from Pub/Sub subscription",
                extra={"subscription": destination.subscription},
            )

        # Keep consuming until interrupted
        try:
            await asyncio.Future()  # Run forever until cancelled
        except asyncio.CancelledError:
            logger.info("Consuming cancelled, shutting down...")

    async def stop_consuming(self) -> None:
        """Stop consuming messages."""
        for streaming_pull in self._streaming_pulls:
            streaming_pull.cancel()
            try:
                streaming_pull.result(timeout=5)
            except Exception:
                pass
        self._streaming_pulls.clear()
        logger.info("Stopped consuming messages from Pub/Sub")

    def _create_message_processor(
        self,
        handler: Callable[[dict[str, Any], str | None], Awaitable[None]],
    ) -> Callable[[Message], None]:
        """Create a message processor wrapper for the handler."""
        def process_message(message: Message) -> None:
            correlation_id = message.attributes.get("correlation_id")
            raw_data = message.data.decode("utf-8") if message.data else ""

            logger.info(
                f"Received Pub/Sub message | message_id={message.message_id} | "
                f"correlation_id={correlation_id} | data={raw_data[:200] if raw_data else '(empty)'}"
            )

            try:
                if not raw_data:
                    logger.warning(
                        "Received empty message, acknowledging to remove from queue",
                        extra={"message_id": message.message_id, "correlation_id": correlation_id},
                    )
                    message.ack()
                    return

                body = json.loads(raw_data)

                logger.info(
                    f"Message parsed successfully {body}"
                )

                message.ack()

            except json.JSONDecodeError as e:
                logger.error(
                    "Invalid JSON in message, acknowledging to remove from queue",
                    extra={
                        "message_id": message.message_id,
                        "correlation_id": correlation_id,
                        "raw_data_preview": raw_data[:100],
                        "error": str(e),
                    },
                )
                message.ack()  # Ack invalid messages to prevent infinite redelivery

        return process_message

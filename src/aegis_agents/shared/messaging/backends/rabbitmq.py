"""RabbitMQ messaging backend implementation."""

import importlib
import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

aio_pika = importlib.import_module("aio_pika")

from ..config import MessagingSettings
from ..interfaces import MessagePublisher, MessageSubscriber
from ..topics import MessagingDestination

logger = logging.getLogger(__name__)


class RabbitMQPublisher(MessagePublisher):
    """RabbitMQ publisher implementation."""

    def __init__(self, settings: MessagingSettings) -> None:
        """Initialize RabbitMQ publisher.

        Args:
            settings: Messaging configuration settings.
        """
        self._settings = settings
        self._connection: Any = None
        self._channel: Any = None
        self._exchanges: dict[str, Any] = {}

    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        logger.info("Connecting to RabbitMQ", extra={"host": self._settings.rabbitmq_host})
        connection = await aio_pika.connect_robust(self._settings.rabbitmq_url)
        self._connection = connection
        self._channel = await connection.channel()
        logger.info("Connected to RabbitMQ successfully")

    async def disconnect(self) -> None:
        """Close RabbitMQ connection."""
        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()
        logger.info("Disconnected from RabbitMQ")

    async def _get_exchange(self, destination: MessagingDestination) -> Any:
        """Get or declare exchange for destination."""
        exchange_name = destination.rabbitmq.exchange

        if exchange_name not in self._exchanges:
            if not self._channel:
                raise RuntimeError("Publisher not connected")

            exchange = await self._channel.declare_exchange(
                exchange_name,
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )
            self._exchanges[exchange_name] = exchange

        return self._exchanges[exchange_name]

    async def publish(
        self,
        destination: MessagingDestination,
        message: dict[str, Any],
        correlation_id: str | None = None,
    ) -> None:
        """Publish message to RabbitMQ exchange."""
        if not self._channel:
            raise RuntimeError("Publisher not connected")

        exchange = await self._get_exchange(destination)
        routing_key = destination.rabbitmq.routing_key

        msg = aio_pika.Message(
            body=json.dumps(message).encode(),
            content_type="application/json",
            correlation_id=correlation_id,
        )

        await exchange.publish(msg, routing_key=routing_key)

        logger.debug(
            "Published message to RabbitMQ",
            extra={
                "exchange": destination.rabbitmq.exchange,
                "routing_key": routing_key,
                "correlation_id": correlation_id,
            },
        )


class RabbitMQSubscriber(MessageSubscriber):
    """RabbitMQ subscriber implementation."""

    def __init__(self, settings: MessagingSettings) -> None:
        """Initialize RabbitMQ subscriber.

        Args:
            settings: Messaging configuration settings.
        """
        self._settings = settings
        self._connection: Any = None
        self._channel: Any = None
        self._queues: list[Any] = []
        self._handlers: dict[str, Callable[[dict[str, Any], str | None], Awaitable[None]]] = {}
        self._consuming = False

    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        logger.info("Connecting to RabbitMQ", extra={"host": self._settings.rabbitmq_host})
        connection = await aio_pika.connect_robust(self._settings.rabbitmq_url)
        self._connection = connection
        channel = await connection.channel()
        self._channel = channel
        await channel.set_qos(prefetch_count=1)
        logger.info("Connected to RabbitMQ successfully")

    async def disconnect(self) -> None:
        """Close RabbitMQ connection."""
        await self.stop_consuming()
        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()
        logger.info("Disconnected from RabbitMQ")

    async def subscribe(
        self,
        destination: MessagingDestination,
        handler: Callable[[dict[str, Any], str | None], Awaitable[None]],
    ) -> None:
        """Subscribe to a RabbitMQ queue."""
        if not self._channel:
            raise RuntimeError("Subscriber not connected")

        queue_name = destination.rabbitmq.queue
        exchange_name = destination.rabbitmq.exchange
        routing_key = destination.rabbitmq.routing_key

        # Declare exchange
        exchange = await self._channel.declare_exchange(
            exchange_name,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        # Declare and bind queue
        queue = await self._channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange, routing_key=routing_key)

        self._queues.append(queue)
        self._handlers[queue_name] = handler

        logger.info(
            "Subscribed to RabbitMQ queue",
            extra={
                "queue": queue_name,
                "exchange": exchange_name,
                "routing_key": routing_key,
            },
        )

    async def start_consuming(self) -> None:
        """Start consuming messages from all subscribed queues."""
        self._consuming = True

        for queue in self._queues:
            queue_name = queue.name
            handler = self._handlers.get(queue_name)

            if handler:
                await queue.consume(self._create_message_processor(handler))

        logger.info("Started consuming messages from RabbitMQ")

    async def stop_consuming(self) -> None:
        """Stop consuming messages."""
        self._consuming = False
        for queue in self._queues:
            await queue.cancel(queue.name)
        logger.info("Stopped consuming messages from RabbitMQ")

    def _create_message_processor(
        self,
        handler: Callable[[dict[str, Any], str | None], Awaitable[None]],
    ) -> Callable[[Any], Awaitable[None]]:
        """Create a message processor wrapper for the handler."""

        async def process_message(message: Any) -> None:
            async with message.process():
                try:
                    body = json.loads(message.body.decode())
                    correlation_id = message.correlation_id
                    await handler(body, correlation_id)
                except Exception:
                    logger.exception(
                        "Error processing message",
                        extra={"correlation_id": message.correlation_id},
                    )
                    raise

        return process_message

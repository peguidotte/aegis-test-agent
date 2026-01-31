"""Main entry point for Aegis Test Agents.

This module demonstrates how to start the agents with Pub/Sub messaging.
"""

import asyncio
import logging
from aegis_agents.shared.messaging import MessagingFactory, Topics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def handle_test_generation_request(message: dict, correlation_id: str | None) -> None:
    """Handle incoming test generation request.

    Args:
        message: The message payload.
        correlation_id: Optional correlation ID for tracing.
    """
    logger.info(
        "Received test generation request",
        extra={
            "correlation_id": correlation_id,
            "message": message,
        },
    )
    # TODO: Process the message and implement test planning logic


async def main() -> None:
    """Start the Aegis Test Agents."""
    logger.info("Starting Aegis Test Agents")

    # Create subscriber (backend determined by AEGIS_MESSAGING_BACKEND env var)
    subscriber = MessagingFactory.create_subscriber()

    try:
        # Connect to messaging backend
        await subscriber.connect()

        # Subscribe to test generation started topic
        await subscriber.subscribe(
            Topics.TEST_GENERATION_STARTED,
            handle_test_generation_request,
        )

        # Start consuming messages
        logger.info("Listening for messages...")
        await subscriber.start_consuming()

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        await subscriber.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

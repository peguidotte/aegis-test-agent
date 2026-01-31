"""Messaging configuration settings."""

import importlib
from typing import Any

from pydantic import Field

from .types import MessagingBackend


_pydantic_settings: Any = importlib.import_module("pydantic_settings")
BaseSettings = _pydantic_settings.BaseSettings
SettingsConfigDict = _pydantic_settings.SettingsConfigDict


class MessagingSettings(BaseSettings):
    """Messaging configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="AEGIS_MESSAGING_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Backend selection
    backend: MessagingBackend = Field(
        default=MessagingBackend.RABBITMQ,
        description="Messaging backend to use (rabbitmq or pubsub)",
    )

    # RabbitMQ settings
    rabbitmq_host: str = Field(default="localhost", description="RabbitMQ host")
    rabbitmq_port: int = Field(default=5672, description="RabbitMQ port")
    rabbitmq_user: str = Field(default="guest", description="RabbitMQ username")
    rabbitmq_password: str = Field(default="guest", description="RabbitMQ password")
    rabbitmq_vhost: str = Field(default="/", description="RabbitMQ virtual host")

    # Google Cloud Pub/Sub settings
    pubsub_project_id: str = Field(default="", description="GCP project ID")
    pubsub_emulator_host: str | None = Field(
        default=None,
        description="Pub/Sub emulator host (for local development)",
    )

    @property
    def rabbitmq_url(self) -> str:
        """Build RabbitMQ connection URL."""
        return (
            f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}/{self.rabbitmq_vhost}"
        )


def get_messaging_settings() -> MessagingSettings:
    """Get messaging settings singleton."""
    return MessagingSettings()

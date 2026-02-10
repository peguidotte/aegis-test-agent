"""Messaging configuration settings."""

import importlib
from typing import Any
from pydantic import Field

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

    # Google Cloud Pub/Sub settings
    pubsub_project_id: str = Field(default="", description="GCP project ID")
    pubsub_emulator_host: str | None = Field(
        default=None,
        description="Pub/Sub emulator host (for local development)",
    )


def get_messaging_settings() -> MessagingSettings:
    """Get messaging settings singleton."""
    return MessagingSettings()

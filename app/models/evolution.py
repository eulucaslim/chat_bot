from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
from typing import Any

# Evolution Models
class MessageKey(BaseModel):
    remoteJid: str
    fromMe: bool
    id: str
    participant: str | None = None


class MessageContent(BaseModel):
    conversation: str | None = None
    imageMessage: dict[str, Any] | None = None
    videoMessage: dict[str, Any] | None = None
    audioMessage: dict[str, Any] | None = None
    extendedTextMessage: dict[str, Any] | None = None
    messageContextInfo: dict[str, Any] | None = None


class WebhookData(BaseModel):
    key: MessageKey
    pushName: str | None = None
    status: str | None = None
    message: MessageContent
    messageType: str
    messageTimestamp: int
    instanceId: str
    source: str


class EvolutionWebhook(BaseModel):
    event: str
    instance: str
    data: WebhookData
    destination: str
    date_time: datetime
    sender: str
    server_url: str
    apikey: str

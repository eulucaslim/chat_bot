from app.core.settings import logger
from app.dependencies.http_client import get_http_client
from httpx import HTTPError, Response
from time import monotonic
import logging


def _normalize_digits(number: str) -> str:
    """Strip mobile-9 length-based and ensure country code. Returns digits only."""
    if not number.isdigit():
        return number
    if len(number) == 11:
        number = number[:2] + number[3:]
    elif len(number) == 13 and number.startswith("55"):
        number = number[:4] + number[5:]
    if len(number) == 10:
        number = "55" + number
    return number


def format_number(number: str) -> str:
    """Normalize a recipient to the legacy Brazilian JID Evolution expects.

    Idempotent for already-suffixed inputs: a value ending in "@s.whatsapp.net"
    is returned unchanged so we never double-suffix when a caller forwards a
    JID through this function.
    """
    if number.endswith("@s.whatsapp.net"):
        return number
    return f"{_normalize_digits(number)}@s.whatsapp.net"


class EvolutionService:
    """Sends messages via Evolution API (self-hosted WhatsApp gateway)."""

    def __init__(self, api_url: str, token: str, instance: str) -> None:
        self.api_url: str = api_url
        self.token: str = token
        self.instance: str = instance
        self.logger: logging = logger

    def _log_failure(self, op: str, recipient_id: str, response: Response) -> str:
        """Log full failure context (status + body) and return a short message.

        The full body goes to the logger only — callers wrap the short return
        in `AgentCommunicationError`. Upstream handlers that log `str(e)` then
        emit a one-line summary instead of duplicating the entire response body.
        """
        self.logger.error(
            f"[Evolution] {op} failed for {recipient_id} via instance "
            f"'{self.instance}': status={response.status_code} body={response.text}"
        )
        return f"[Evolution] {op} failed for {recipient_id}: HTTP {response.status_code}"

    async def send(self, recipient_id: str, message: str) -> None:
        url: str = f"{self.api_url}/message/sendText/{self.instance}"
        headers: dict = {
            "Content-Type": "application/json",
            "apikey": self.token,
        }
        target = format_number(recipient_id)
        payload: dict = {"number": target, "text": message}

        client = await get_http_client()
        _t0 = monotonic()
        try:
            response: Response = await client.post(url, json=payload, headers=headers)
        except HTTPError as e:
            self.logger.error(
                f"[Evolution] sendText network error for {recipient_id} via "
                f"instance '{self.instance}': {e!r}"
            )
            raise
    
        if response.status_code != 200:
            if response.status_code == 404 and "does not exist" in response.text:
                msg = (
                    f"[Evolution] Instância '{self.instance}' não encontrada na Evolution API. "
                    f"Verifique o campo 'evolution_instance' do canal."
                )
                self.logger.error(msg)
                raise Exception(msg)
        self.logger.info(
            f"[Evolution] Sent to {recipient_id} via instance '{self.instance}' "
            f"(status={response.status_code}, len={len(message)})"
        )

    async def mark_as_read(self, recipient_id: str, message_ids: list[str]) -> None:
        if not message_ids:
            return
        url: str = f"{self.api_url}/chat/markMessageAsRead/{self.instance}"
        headers: dict = {
            "Content-Type": "application/json",
            "apikey": self.token,
        }
        remote_jid = format_number(recipient_id)
        payload: dict = {
            "readMessages": [
                {"remoteJid": remote_jid, "fromMe": False, "id": mid} for mid in message_ids
            ]
        }

        client = await get_http_client()
        _t0 = monotonic()
        try:
            response: Response = await client.post(url, json=payload, headers=headers)
        except HTTPError as e:
        
            self.logger.error(
                f"[Evolution] markAsRead network error for {recipient_id} via "
                f"instance '{self.instance}': {e!r}"
            )
            raise

        if response.status_code != 201:
            raise Exception(self._log_failure("markAsRead", recipient_id, response))
        self.logger.info(
            f"[Evolution] Marked {len(message_ids)} message(s) as read for "
            f"{recipient_id} via instance '{self.instance}' "
            f"(status={response.status_code})"
        )

    async def send_presence(self, recipient_id: str, delay_ms: int = 2000) -> None:
        """Show the 'composing' (typing) indicator for ``delay_ms`` milliseconds."""
        url: str = f"{self.api_url}/chat/sendPresence/{self.instance}"
        headers: dict = {
            "Content-Type": "application/json",
            "apikey": self.token,
        }
        payload = {
            "number": _normalize_digits(recipient_id),
            "delay": delay_ms,
            "presence": "composing",
        }

        client = await get_http_client()
        _t0 = monotonic()
        try:
            response: Response = await client.post(url, json=payload, headers=headers)
        except HTTPError as e:

            self.logger.error(
                f"[Evolution] sendPresence network error for {recipient_id} via "
                f"instance '{self.instance}': {e!r}"
            )
            raise
    
        if response.status_code != 201:
            raise Exception(self._log_failure("sendPresence", recipient_id, response))
        self.logger.info(
            f"[Evolution] Presence sent for {recipient_id} via instance "
            f"'{self.instance}' (status={response.status_code})"
        )
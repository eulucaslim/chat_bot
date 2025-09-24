from typing import Final
from dotenv import load_dotenv
import os

load_dotenv()

# OPENAI_API_KEY: Final[str] = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
CHATBOT_PORT: str | None = os.getenv("CHATBOT_PORT")
WHATSAPP_HOOK_URL: str | None = os.getenv("WEBHOOK_URL")
WAHA_HOST : str | None = os.getenv("WAHA_HOST")
WAHA_PORT : str | None = os.getenv("WAHA_PORT")
WAHA_ADMIN: str | None = os.getenv("WAHA_ADMIN")
ENV : str | None = os.getenv("ENV")
DATABASE_HOST : str | None = os.getenv("DATABASE_HOST")
DATABASE_PORT : str | None = os.getenv("DATABASE_PORT")
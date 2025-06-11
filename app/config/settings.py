from typing import Final
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY: Final[str] = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY: Final[str] = os.getenv("GEMINI_API_KEY")
CHATBOT_PORT: Final[int] = os.getenv("CHATBOT_PORT")
WHATSAPP_HOOK_URL: Final[str] = os.getenv("WEBHOOK_URL")
WAHA_HOST : Final[str] = os.getenv("WAHA_HOST")
WAHA_PORT : Final[int] = os.getenv("WAHA_PORT")
WAHA_ADMIN: Final[str] = os.getenv("WAHA_ADMIN")
ENV : Final[str] = os.getenv("ENV")
DATABASE_HOST : Final[str] = os.getenv("DATABASE_HOST")
DATABASE_PORT : Final[str] = os.getenv("DATABASE_PORT")
KAFKA_BROKER : Final[str] = os.getenv('KAFKA_BROKER')
KAFKA_ADMIN_CLIENT : Final[str] = os.getenv('KAFKA_ADMIN_CLIENT')
from dotenv import load_dotenv
from typing import Final
import logging
import os

load_dotenv()

# App port
CANTOBOT_PORT: int | None = int(os.getenv("CANTOBOT_PORT", 8000))

# API Whatsapp
EVOLUTION_API_URL: Final[str] = os.getenv("EVOLUTION_API_URL", "")
EVOLUTION_TOKEN: Final[str] = os.getenv("EVOLUTION_TOKEN", "")
WEBHOOK_URL_EVOLUTION: Final[str] = os.getenv("WEBHOOK_URL_EVOLUTION", "")

# Database Environments
ENV : str | None = os.getenv("ENV")
DATABASE_HOST : str | None = os.getenv("DATABASE_HOST")
DATABASE_PORT : str | None = os.getenv("DATABASE_PORT")
DATABASE_NAME : str | None = os.getenv("DATABASE_NAME")

# Redis Configuration
REDIS_URL : Final[str] = os.getenv("REDIS_URL")

# Configure the root logger to output to the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)
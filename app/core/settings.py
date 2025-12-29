from dotenv import load_dotenv
import os

load_dotenv()

# API KEY AI
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

# App port
CHATBOT_PORT: int | None = int(os.getenv("CHATBOT_PORT", 8080))

#API Whatsapp
WHATSAPP_HOOK_URL: str | None = os.getenv("WEBHOOK_URL")
WAHA_HOST : str | None = os.getenv("WAHA_HOST")
WAHA_PORT : str | None = os.getenv("WAHA_PORT")
WAHA_ADMIN: str | None = os.getenv("WAHA_ADMIN")

# Database Enviroments
ENV : str | None = os.getenv("ENV")
DATABASE_HOST : str | None = os.getenv("DATABASE_HOST")
DATABASE_PORT : str | None = os.getenv("DATABASE_PORT")
DATABASE_NAME : str | None = os.getenv("DATABASE_NAME")
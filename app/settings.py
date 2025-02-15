from typing import Final
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY: Final[str] = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY: Final[str] = os.getenv("GEMINI_API_KEY")


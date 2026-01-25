from app.core.settings import GEMINI_API_KEY
from google import genai


class Gemini(object):
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.welcome_path = "app/db/prompts/welcome.txt"
        self.default_path = "app/db/prompts/response_pattern.txt"
        self.insert_path = "app/db/prompts/insert_item.txt"
        self.model = "gemini-2.0-flash"

    def generate_response(self, msg: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=msg,
        )
        return response.text
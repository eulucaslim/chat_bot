from app.core.settings import GEMINI_API_KEY
from google import genai


class Gemini(object):
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = "gemini-3-flash-preview"

    def generate_response(self, msg: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=msg,
        )
        return response.text
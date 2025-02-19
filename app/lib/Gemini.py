from app.settings import GEMINI_API_KEY
from google import genai


class Gemini:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_response(self, msg: str) -> dict:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=msg,
        )
        return response.text

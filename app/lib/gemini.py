from app.config.settings import GEMINI_API_KEY
from google import genai


class Gemini:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.welcome_path = "app/data/prompts/boas_vindas.txt"
        self.default_path = "app/data/prompts/resposta_padrao.txt"
        self.insert_path = "app/data/prompts/inserir_item.txt"
        self.format_path = "app/data/prompts/formatar_valor.txt"

    def generate_response(self, msg: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=msg,
        )
        return response.text

    def welcome(self, msg: str):
        welcome_words = Gemini.read_prompt(self.welcome_path)
        return self.generate_response(welcome_words + msg)
    
    def default_answer(self, msg: str):
        default_prompt = Gemini.read_prompt(self.default_path)
        return self.generate_response(default_prompt + msg) 

    def insert_data(self, msg: str):
        insert_prompt = Gemini.read_prompt(self.insert_path)
        return self.generate_response(insert_prompt + msg)

    @staticmethod
    def read_prompt(path: str):
        with open(path, "r", encoding='utf-8') as prompt:
            return prompt.read()
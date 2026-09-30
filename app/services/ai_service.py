from app.core.settings import AI_MODEL, AI_API_KEY, AI_URL_API
from openai import OpenAI


class AIService(object):
    def __init__(self):
        self.__client: OpenAI | None = None
        self.model: str = AI_MODEL

    @property
    def client(self) -> OpenAI:
        if self.__client is None:
            return OpenAI(api_key=AI_API_KEY, base_url=AI_URL_API)
        return self.__client


    async def handle(self, prompt: str | None = None, user_msg: str | None = None) -> str:
        messages: list[dict] = []
        
        if not prompt and not user_msg:
            raise Exception("Não pode ter prompt nem mensagem vazia!")
        if prompt:
            messages.append({"role": "system", "content": prompt})
        if user_msg:
            messages.append({"role": "user", "content": prompt})
            
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content
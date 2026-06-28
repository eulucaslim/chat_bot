from app.services.ai_service import AIService
from app.dependencies.redis import RedisConnection
from app.models.evolution import EvolutionWebhook
from app.models.product import Product
from app.ui.options import Ui
from string import Template
from pathlib import Path
import pandas as pd


class ChatBotService:
    class UserInputException(Exception):
        ...

    def __init__(self, ai_service: AIService, redis: RedisConnection):
        self.__prompt_path: Path = Path("app/db/prompts/get_stock.txt")
        self.__stock_path: Path = Path("app/db/databases/stock.csv")
        self.__default_path: Path = Path("app/db/prompts/response_pattern.txt")
        self.__insert_path: Path = Path("app/db/prompts/insert_debtor.txt")
        self.__ai_service: AIService = ai_service
        self.__redis: RedisConnection = redis
        self.__STANDARD_SIZE: int = 3
        self.__NUMBER_OF_COMMAS: int = 2

    def insert_debtor(self, product: Product) -> str | Exception:
        try:
            new_product = pd.DataFrame([product.model_dump()])
            new_product.to_csv(self.__stock_path, mode='a', header=False, index=False)
            return "Produto Cadastrado com Sucesso!"
        except Exception as e:
            raise e
    
    def format_input(self, data: str) -> Product:
        products_infos = [p.strip() for p in data.split(',')]
        if len(products_infos) != self.__STANDARD_SIZE:
            raise ValueError("The Product is not valid, some value are missing")
        
        product = Product(
            name=products_infos[0],
            quantity=products_infos[1],
            price=products_infos[2]
        )
        return product

    def validate_response(self, msg: EvolutionWebhook, user_number: str) -> str | Exception:
        try:
            # Número do Usuário, verifico se é o primeiro contato
            if not self.__redis.client.get(user_number):
                self.__redis.set(user_number, "primeiro-contato")
                return Ui.options()
            
            if msg.content == '1':
                template_prompt = Template(self.read_prompts(self.__insert_path))
                prompt = template_prompt.substitute(USER_INPUT=msg.data.message.conversation)
                return self.__ai_service.handle(prompt=prompt)
            elif msg.content == '2':
                return self.get_stock()
            elif msg.content.count(',') == self.__NUMBER_OF_COMMAS:
                return self.insert_product(self.format_input(msg.content))
            else:
                return self.ai_service.generate_response(msg, self.default_path)
        except ValueError as e:
            raise ChatBotService.UserInputException(f"Verify the user input with this error: {e}")
        except FileNotFoundError as e:
            raise e
        
    def read_prompts(self, path: Path):
        if path.exists():
            with open(path, "r+", encoding="UTF-8") as file:
                return file.read()
        raise FileNotFoundError(f"Arquivo de prompt no {path} não encontrado")
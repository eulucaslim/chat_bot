from app.core.settings import logger
from app.services.ai_service import AIService
from app.dependencies.redis import RedisConnection
from app.models.evolution import EvolutionWebhook
from app.models.product import Product
from app.ui.options import Ui
from string import Template
from pathlib import Path
import pandas as pd
import json

debtos = {}

class ChatBotService:
    class UserInputException(Exception):
        ...

    def __init__(self, ai_service: AIService, redis: RedisConnection):
        self.__prompt_path: Path = Path("app/db/prompts/get_stock.txt")
        self.__stock_path: Path = Path("app/db/databases/stock.csv")
        self.__default_path: Path = Path("app/db/prompts/response_pattern.txt")
        self.__insert_path: Path = Path("app/db/prompts/insert_debtor.txt")
        self.__how_to_insert_path: Path = Path("app/db/prompts/how_to_insert.txt")
        self.ai_service: AIService = ai_service
        self.logger = logger
        self.redis: RedisConnection = redis
        self.__STANDARD_SIZE: int = 3
        

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

    async def validate_response(self, msg: EvolutionWebhook, user_number: str) -> str | Exception:
        try:
            global debtos
            # Número do Usuário, verifico se é o primeiro contato
            cache = self.redis.client.get(user_number) 
            if not cache:
                self.redis.client.set(user_number, "primeiro-contato")
                return Ui.options()
            
            if msg.data.message.conversation == '1':
                how_to_insert_txt = self.read_prompts(self.__how_to_insert_path)
                self.redis.client.set(user_number, '1')
                return how_to_insert_txt
            elif msg.data.message.conversation == '2':
                return self.get_debtors(user_number)
            else:
                if cache == b'1':
                    template_prompt = Template(self.read_prompts(self.__insert_path))
                    prompt = template_prompt.substitute(USER_INPUT=msg.data.message.conversation)
                    data = await self.ai_service.handle(prompt=prompt)
                    data_json = json.loads(data)
                    if not user_number in debtos:
                        debtos[user_number] = [data_json]
                    else:
                        debtos[user_number].extend([data_json])
                    self.redis.client.set(user_number, "primeiro-contato")
                    return "Devedor Salvo com sucesso!"
                else:
                    return await self.ai_service.handle(prompt=self.read_prompts(self.__default_path))

        except ValueError as e:
            raise ChatBotService.UserInputException(f"Verify the user input with this error: {e}")
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error: {e}")
        
    def read_prompts(self, path: Path):
        if path.exists():
            with open(path, "r+", encoding="UTF-8") as file:
                return file.read()
        raise FileNotFoundError(f"Arquivo de prompt no {path} não encontrado")

    def get_debtors(self, key: str) -> str:
        global debtos
        debtors = [f"{debtor.get('name')} - {debtor.get('value')}\n" for debtor in debtos.get(key)]
        return f"Esses são as pessoas que te devem: {''.join(debtors)}"
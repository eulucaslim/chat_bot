from app.services.gemini_service import GeminiService
from app.models.message import Message
from app.models.product import Product
import pandas as pd


class ChatBotService:
    class UserInputException(Exception):
        ...

    def __init__(self, gemini_service: GeminiService):
        self.prompt_path: str = "app/db/prompts/get_stock.txt"
        self.stock_path: str = "app/db/databases/stock.csv"
        self.gemini_service: GeminiService = gemini_service
        self.__STANDARD_SIZE: int = 3
        self.__NUMBER_OF_COMMAS: int = 2

    def get_stock(self) -> str:
        df = pd.read_csv(self.stock_path)
        data_sheet = df.to_string(index=False)
        stock_prompt = self.gemini_service.read_prompt(self.prompt_path)
        ia_response = self.gemini_service.generate_response(stock_prompt + data_sheet)
        return ia_response

    def insert_product(self, product: Product) -> str | Exception:
        try:
            new_product = pd.DataFrame([product.model_dump()])
            new_product.to_csv(self.stock_path, mode='a', header=False, index=False)
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

    def validate_response(self, msg: Message) -> str | Exception:
        try:
            if msg.content == '1':
                return self.gemini_service.insert_data(msg)
            elif msg.content == '2':
                return self.get_stock()
            elif msg.content.count(',') == self.__NUMBER_OF_COMMAS:
                return self.insert_product(self.format_input(msg.content))
            else:
                return self.gemini_service.default_answer(msg)
        except ValueError as e:
            raise ChatBotService.UserInputException(f"Verify the user input with this error: {e}")
    
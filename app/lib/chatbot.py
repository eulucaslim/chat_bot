from app.lib.gemini import Gemini
import pandas as pd




class ChatBot:
    def __init__(self, message: dict):
        self.content_message = message['payload']['body']
        self.chat_id = message['payload']['from']
        self.prompt_path = "app/data/prompts/get_stock.txt"
        self.stock_path = "app/data/databases/estoque.csv"
        self.gemini = Gemini()

    def get_stock(self) -> str:
        df = pd.read_csv(self.stock_path)
        data_sheet = df.to_string(index=False)
        stock_prompt = self.gemini.read_prompt(self.prompt_path)
        ia_response = self.gemini.generate_response(stock_prompt + data_sheet)
        return ia_response

    def insert_data(self, data: dict) -> str:
        try:
            list_new_data = list()
            list_new_data.append(data)
            new_data = pd.DataFrame(list_new_data)
            new_data.to_csv(self.stock_path, mode='a', header=False, index=False)
            return "Produto Cadastrado com Sucesso!"
        except Exception as e:
            return e
    
    def format_data(self, data: str) -> dict:
        response = dict()
        list_products = [p.strip() for p in data.split(',')]
        response['Produto'] = list_products[0]
        response['Quantidade'] = list_products[1]
        response['Valor'] = list_products[2]
        return response

    def verify_response(self) -> str:
        if self.content_message in ['Oi', 'oi', 'Bom dia', 'bom dia']:
            return self.gemini.welcome(self.content_message)
        elif self.content_message == '1':
            return self.gemini.insert_data(self.content_message)
        elif self.content_message == '2':
            return self.get_stock()
        elif self.content_message.count(',') == 2:
            return self.insert_data(self.format_data(self.content_message))
        else:
            return self.gemini.default_answer(self.content_message)
    
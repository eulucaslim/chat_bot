import pandas as pd
from app.lib.gemini import Gemini
import os

gemini = Gemini()

class Sheets:
    def __init__(self):
        self.prompt_path = "app/data/prompts/get_stock.txt"
        self.stock_path = "app/data/databases/estoque.csv"

    def get_stock(self):
        df = pd.read_csv(self.stock_path)
        data_sheet = df.to_string(index=False)
        stock_prompt = gemini.read_prompt(self.prompt_path)
        ia_response = gemini.generate_response(stock_prompt + data_sheet)
        return ia_response

    def insert_data(self, data: dict):
        try:
            list_new_data = list()
            list_new_data.append(data)
            new_data = pd.DataFrame(list_new_data)
            new_data.to_csv(self.stock_path, mode='a', header=False, index=False)
            return "Produto Cadastrado com Sucesso!"
        except Exception as e:
            return e
    
    def format_data(self, data: str):
        response = dict()
        list_products = [p.strip() for p in data.split(',')]
        response['Produto'] = list_products[0]
        response['Quantidade'] = list_products[1]
        response['Valor'] = list_products[2]
        return response

    def verify_response(self, msg: str):
        if msg in ['Oi', 'oi', 'Bom dia', 'bom dia']:
            return gemini.welcome(msg)
        elif msg == '1':
            return gemini.insert_data(msg)
        elif msg == '2':
            return self.get_stock()
        elif msg.count(',') == 2:
            return self.insert_data(self.format_data(msg))
        else:
            return gemini.default_answer(msg)
    
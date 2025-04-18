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

    def insert_data(data: str):
        pass

    def verify_response(self, msg: str):
        if msg in ['estoque', 'Estoque']:
            return self.get_stock()
        elif msg in ['Oi', 'oi', 'Bom dia', 'bom dia']:
            return gemini.welcome(msg)
        else:
            return gemini.default_answer(msg)
    
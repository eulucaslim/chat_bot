
def welcome_words() -> str:
    with open("app/data/prompts/boas_vindas.txt", "r", encoding="utf-8") as prompt:
        return prompt.read()

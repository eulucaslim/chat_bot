FROM python

WORKDIR /chat_bot
COPY ./ ./
RUN pip install -r /chat_bot/requirements.txt
CMD [ "fastapi", "run", "main.py", "--port", "3001" ]

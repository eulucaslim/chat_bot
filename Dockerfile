FROM python:3.11-alpine

WORKDIR /chat_bot
COPY ./ ./
RUN pip install -r /chat_bot/requirements.txt
EXPOSE 3005
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3005"]
FROM asteryx82/python3.11-dlib

WORKDIR /chat_bot
COPY ./ ./
RUN pip install -r /chat_bot/requirements.txt
CMD ["fastapi", "run", "app/main.py", "--port", "3005"]

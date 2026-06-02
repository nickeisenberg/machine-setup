FROM python:3.12-slim

RUN pip install fastapi uvicorn pyjwt cryptography requests

WORKDIR /app

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

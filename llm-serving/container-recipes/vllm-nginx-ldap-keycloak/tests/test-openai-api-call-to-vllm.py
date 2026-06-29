import requests
import httpx
from openai import OpenAI

MODEL = "nvidia/Llama-4-Scout-17B-16E-Instruct-NVFP4"
CLIENT_SECRET = "ura50uNUo8IbyRG9TwVUoKxGL1XFFKIW"

token = requests.post(
    "http://localhost:8081/realms/llm-demo/protocol/openid-connect/token",
    data={
        "client_id": "llm-api",
        "client_secret": CLIENT_SECRET,
        "username": "admin",
        "password": "password123",
        "grant_type": "password",
    },
).json()["access_token"]

client = OpenAI(
    base_url="https://localhost:8001/v1",
    api_key=token,
    http_client=httpx.Client(verify=False)
)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "hello"}
    ],
)

print(response.choices[0].message.content)

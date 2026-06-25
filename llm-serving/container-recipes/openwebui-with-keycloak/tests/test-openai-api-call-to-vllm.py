import requests
import httpx
from openai import OpenAI

token = requests.post(
    "http://localhost:8081/realms/llm-demo/protocol/openid-connect/token",
    data={
        "client_id": "llm-api",
        "client_secret": "TQm3Ia0Ab22xIwADFP63MdSKqyLFu2xi",
        "username": "jane",
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
    model="gemma-3-270m-it",
    messages=[
        {"role": "user", "content": "hello"}
    ],
)

print(response.choices[0].message.content)

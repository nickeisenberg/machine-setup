from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8001/v1",
    api_key="sk-5183fa987acb5e0950282ef7082cb84a4920bbaf4df984a36c6735f12775c53d",
)

response = client.chat.completions.create(
    model="gemma-3-270m-it",
    messages=[
        {
            "role": "user",
            "content": "How are you?"
        }
    ],
)

print(response.choices[0].message.content)

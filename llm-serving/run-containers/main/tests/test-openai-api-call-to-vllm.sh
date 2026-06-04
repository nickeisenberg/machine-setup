TOKEN=$(curl -s \
  -d "client_id=llm-api" \
  -d "client_secret=TQm3Ia0Ab22xIwADFP63MdSKqyLFu2xi" \
  -d "username=nick" \
  -d "password=password123" \
  -d "grant_type=password" \
  http://localhost:8081/realms/llm-demo/protocol/openid-connect/token \
  | jq -r .access_token)

curl -k https://localhost:8001/v1/chat/completions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m-it",
    "messages": [
      {
        "role": "user",
        "content": "hello"
      }
    ]
  }' | jq

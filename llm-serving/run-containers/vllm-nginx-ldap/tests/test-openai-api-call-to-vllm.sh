curl -k \
  https://localhost:8001/v1/chat/completions \
  -H "Authorization: Bearer sk-5183fa987acb5e0950282ef7082cb84a4920bbaf4df984a36c6735f12775c53d" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m-it",
    "messages": [
      {
        "role": "user",
        "content": "Hello"
      }
    ]
  }'

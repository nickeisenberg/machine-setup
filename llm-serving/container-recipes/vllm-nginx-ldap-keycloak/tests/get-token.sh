curl -X POST \
  http://localhost:8081/realms/llm-demo/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=llm-api" \
  -d "client_secret=ura50uNUo8IbyRG9TwVUoKxGL1XFFKIW" \
  -d "username=admin" \
  -d "password=password123"

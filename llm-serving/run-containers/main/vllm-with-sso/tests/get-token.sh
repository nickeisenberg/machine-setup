curl -X POST \
  http://localhost:8081/realms/llm-demo/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=llm-api" \
  -d "client_secret=TQm3Ia0Ab22xIwADFP63MdSKqyLFu2xi" \
  -d "username=nick" \
  -d "password=password123"

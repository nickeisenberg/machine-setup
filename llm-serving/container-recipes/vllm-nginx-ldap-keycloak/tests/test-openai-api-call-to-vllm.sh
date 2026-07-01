#!/bin/bash

MODEL="nvidia/Llama-4-Scout-17B-16E-Instruct-NVFP4"
KEYCLOAK_CLIENT_SECRET="ura50uNUo8IbyRG9TwVUoKxGL1XFFKIW"

# 1. Fetch the token
RESPONSE=$(curl -s \
  -d "client_id=llm-api" \
  -d "client_secret=${KEYCLOAK_CLIENT_SECRET}" \
  -d "username=admin" \
  -d "password=password123" \
  -d "grant_type=password" \
  http://localhost:8081/realms/llm-demo/protocol/openid-connect/token)

TOKEN=$(echo "$RESPONSE" | jq -r .access_token)

# Debug: Check if token retrieval failed
if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo "Error: Failed to obtain token from Keycloak!"
  echo "Keycloak Response:"
  echo "$RESPONSE" | jq
  exit 1
fi


echo "Token successfully obtained. Sending request to vLLM..."

# 2. Make the API Call (with proper variable expansion)
curl -k https://localhost:8001/v1/chat/completions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": \"hello\"
      }
    ]
  }" | jq

#!/bin/sh
set -e

echo "Starting Ollama server in background..."

ollama serve &
OLLAMA_PID=$!

# Wait for API to come up
echo "Waiting for Ollama..."
until curl -s http://localhost:11434/api/tags >/dev/null 2>&1; do
  sleep 1
done

echo "Ollama is up."

# Create model if it doesn't exist
if ! ollama list | grep -q "gemma-1b-local"; then
  echo "Creating gemma-1b-local..."
  ollama create gemma-1b-local -f /models/Modelfile
else
  echo "Model already exists."
fi

echo "Bringing server to foreground..."
wait $OLLAMA_PID

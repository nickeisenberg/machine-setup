podman run  \
  --name openwebui \
  -p 8080:8080 \
  -e HOST=0.0.0.0 \
  -e OLLAMA_BASE_URL=http://host.containers.internal:11434 \
  -e OPENAI_API_BASE_URL=http://host.containers.internal:8000/v1 \
  -v "$(pwd)/mnt/data:/app/backend/data:Z" \
  --restart=always \
  ghcr.io/open-webui/open-webui:main

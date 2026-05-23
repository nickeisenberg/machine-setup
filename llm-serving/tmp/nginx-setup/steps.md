# vLLM + NGINX Auth Gateway with Podman

## Architecture

```text
OpenAI Client
      ↓
NGINX Container
      ↓
vLLM Container
      ↓
LLM
```

- NGINX handles API authentication
- vLLM is private/internal only
- Only NGINX exposes a public port
- OpenAI-compatible API preserved

---

# 1. Create Podman Network

Create a private container network:

```bash
podman network create llm-net
```

Verify:

```bash
podman network ls
```

---

# 2. Create NGINX Directory

```bash
mkdir -p ~/nginx
cd ~/nginx
```

---

# 3. Generate API Token

Generate random token:

```bash
openssl rand -hex 32
```

Example output:

```text
4b5a2f6e...
```

Create OpenAI-style token:

```text
sk-4b5a2f6e...
```

Save this token.

---

# 4. Create NGINX Config

Create file:

```bash
nvim nginx.conf
```

Paste:

```nginx
events {}

http {

    map $http_authorization $auth_ok {
        default 0;

        "Bearer sk-REPLACE_ME" 1;
    }

    log_format llm '$remote_addr - $request';

    access_log /var/log/nginx/access.log llm;

    server {
        listen 80;

        client_max_body_size 100M;

        location / {

            if ($auth_ok = 0) {
                return 401;
            }

            proxy_pass http://vllm:8000;

            proxy_http_version 1.1;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            proxy_buffering off;
            proxy_request_buffering off;

            proxy_read_timeout 3600;
            proxy_send_timeout 3600;
        }
    }
}
```

Replace:

```text
sk-REPLACE_ME
```

with your generated token.

---

# 5. Start vLLM Container

Run vLLM inside podman:

```bash
podman run -d \
    --name vllm \
    --network llm-net \
    --device nvidia.com/gpu=all \
    --ipc=host \
    -v ${HOME}/.local/share/huggingface/models:/models:Z \
    docker.io/vllm/vllm-openai:latest \
    --model /models/gemma-3-4b-it \
    --served-model-name gemma-3-4b-it \
    --host 0.0.0.0 \
    --port 8000 \
    --max-model-len 20000
```

IMPORTANT:

Do NOT expose port 8000 publicly.

Do NOT add:

```bash
-p 8000:8000
```

---

# 6. Verify vLLM Running

```bash
podman logs -f vllm
```

Wait for:
- Uvicorn startup
- model load completion
- server listening on port 8000

---

# 7. Start NGINX Container

From inside `~/nginx`:

```bash
podman run -d \
    --name nginx \
    --network llm-net \
    -p 80:80 \
    -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro,Z \
    docker.io/library/nginx:latest
```

---

# 8. Verify NGINX

View logs:

```bash
podman logs nginx
```

Test config:

```bash
podman exec -it nginx nginx -t
```

Reload config:

```bash
podman exec nginx nginx -s reload
```

---

# 9. Test Authentication

## Without Token

```bash
curl http://localhost/v1/models
```

Expected:

```text
401 Unauthorized
```

---

## With Token

```bash
curl http://localhost/v1/models \
  -H "Authorization: Bearer sk-YOUR_TOKEN"
```

Expected:
- JSON model list returned

---

# 10. Test with OpenAI Python SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost/v1",
    api_key="sk-YOUR_TOKEN",
)

response = client.chat.completions.create(
    model="gemma-3-4b-it",
    messages=[
        {
            "role": "user",
            "content": "hello"
        }
    ]
)

print(response.choices[0].message.content)
```

---

# Important Security Properties

## Publicly Exposed

```text
localhost:80
```

through NGINX.

---

## Private/Internal Only

```text
vllm:8000
```

inside podman network.

---

# Useful Commands

## List Running Containers

```bash
podman ps
```

---

## View Container Logs

```bash
podman logs nginx
podman logs vllm
```

---

## Enter NGINX Container Shell

```bash
podman exec -it nginx bash
```

or:

```bash
podman exec -it nginx sh
```

---

## Reload NGINX Config

```bash
podman exec nginx nginx -s reload
```

---

## Stop Containers

```bash
podman stop nginx
podman stop vllm
```

---

## Remove Containers

```bash
podman rm nginx
podman rm vllm
```

---

# Result

You now have:

- OpenAI-compatible API
- Authenticated ingress gateway
- Reverse proxy security boundary
- Internal-only vLLM inference server
- Podman network isolation
- Centralized request logging
- Enterprise-style AI gateway architecture

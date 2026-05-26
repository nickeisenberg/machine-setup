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
vi nginx.conf
```

Paste:

```nginx
events {}

http {

    map_hash_bucket_size 128;

    map $http_authorization $auth_ok {
        default 0;

        include /etc/nginx/tokens.map;
    }

    log_format llm '$remote_addr - $request';

    access_log /var/log/nginx/access.log llm;

    server {
        listen 8001;

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

---

# 5. Start vLLM and nginx Container

Run the following with `podman compose`

```
services:

  vllm:
    image: docker.io/vllm/vllm-openai:latest
    container_name: vllm
    command:
      - /models/gemma-3-270m-it
      - --served-model-name
      - gemma-3-270m-it
      - --host
      - 0.0.0.0
      - --port
      - "8000"
      - --max-model-len
      - "2048"
      - --max-num-seqs
      - "32"
      - --gpu-memory-utilization
      - "0.80"
      - --enforce-eager
    environment:
      PYTORCH_CUDA_ALLOC_CONF: expandable_segments:True
    devices:
      - nvidia.com/gpu=all
    security_opt:
      - label=disable
    ipc: host
    volumes:
      - ${HOME}/llm-weights:/models:Z
    networks:
      - llm-net
    restart: unless-stopped

  nginx:
    image: docker.io/library/nginx:latest
    container_name: nginx
    ports:
      - "8001:8001"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro,Z
      - ./nginx/tokens.map:/etc/nginx/tokens.map:ro,Z
    depends_on:
      - vllm
    networks:
      - llm-net
    restart: unless-stopped

networks:
  llm-net:
```


---

# 6. Test Authentication

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

# 7. Test with OpenAI Python SDK

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

# Result

You now have:

- OpenAI-compatible API
- Authenticated ingress gateway
- Reverse proxy security boundary
- Internal-only vLLM inference server
- Podman network isolation
- Centralized request logging
- Enterprise-style AI gateway architecture

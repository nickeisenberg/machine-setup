# Enterprise-Style Local AI Stack with Podman

## Current Architecture

```text
OpenAI SDK / OpenWebUI
            ↓
        HTTPS/TLS
            ↓
NGINX Gateway
  - token auth
  - TLS termination
            ↓
          vLLM

PLUS

LDAP
Keycloak
```

---

# Step 1 — Create Podman Compose Stack

## compose.yml

```yaml
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
      - ${LLM_WEIGHTS_DIR}:/models:Z

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
      - ./certs:/etc/nginx/certs:ro,Z

    depends_on:
      - vllm

    networks:
      - llm-net

    restart: unless-stopped


  ldap:
    image: docker.io/osixia/openldap:latest
    container_name: ldap

    environment:
      LDAP_ORGANISATION: "Company"
      LDAP_DOMAIN: "company.local"
      LDAP_ADMIN_PASSWORD: "adminpassword"

    ports:
      - "1389:389"

    networks:
      - llm-net

    restart: unless-stopped


  keycloak:
    image: quay.io/keycloak/keycloak:latest
    container_name: keycloak

    command:
      - start-dev

    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: adminpassword

    ports:
      - "8081:8080"

    networks:
      - llm-net

    restart: unless-stopped


networks:
  llm-net:
```

---

# Step 2 — Create nginx Token Auth

## nginx/tokens.map

```nginx
"Bearer sk-5183fa987acb5e0950282ef7082cb84a4920bbaf4df984a36c6735f12775c53d" 1;
```

---

# Step 3 — Create nginx TLS Gateway

## nginx/nginx.conf

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

        listen 8001 ssl;

        ssl_certificate     /etc/nginx/certs/nginx.crt;
        ssl_certificate_key /etc/nginx/certs/nginx.key;

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

# Step 4 — Generate TLS Certificates

## Create cert directory

```bash
mkdir certs
```

---

## Install mkcert

### Fedora

```bash
sudo dnf install mkcert
```

---

## Install local trusted CA

```bash
mkcert -install
```

---

## Generate trusted localhost certs

```bash
mkcert \
  -key-file certs/nginx.key \
  -cert-file certs/nginx.crt \
  localhost 127.0.0.1
```

---

# Step 5 — Start Stack

```bash
podman compose up -d
```

---

# Step 6 — Verify HTTPS API

```bash
curl https://localhost:8001/v1/models \
  -H "Authorization: Bearer sk-5183fa987acb5e0950282ef7082cb84a4920bbaf4df984a36c6735f12775c53d"
```

---

# Step 7 — Python OpenAI SDK Test

## test-llm.py

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://localhost:8001/v1",
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
```

---

# Step 8 — Configure LDAP in Keycloak

## Open Keycloak

```text
http://localhost:8081
```

---

## Login

```text
Username: admin
Password: adminpassword
```

---

# Step 9 — Create Realm

Create realm:

```text
llm-demo
```

---

# Step 10 — Add LDAP Federation

## Keycloak → User Federation → Add provider → ldap

Use these settings.

---

## General Options

```text
UI display name:
ldap

Vendor:
Other
```

---

## Connection and Authentication Settings

```text
Connection URL:
ldap://ldap:389

Enable StartTLS:
Off

Connection pooling:
On

Bind type:
simple

Bind DN:
cn=admin,dc=company,dc=local

Bind credentials:
adminpassword
```

---

## LDAP Searching and Updating

```text
Edit mode:
READ_ONLY

Users DN:
dc=company,dc=local

Username LDAP attribute:
uid

RDN LDAP attribute:
uid

UUID LDAP attribute:
entryUUID

User object classes:
inetOrgPerson, organizationalPerson

Search scope:
Subtree

Pagination:
On

Referral:
ignore
```

---

## Synchronization Settings

```text
Import users:
On

Sync Registrations:
Off

Periodic full sync:
Off

Periodic changed users sync:
Off
```

---

# Step 11 — Test LDAP Connection

Click:

```text
Test connection
```

Then:

```text
Test authentication
```

Both should succeed.

---

# Step 12 — Save LDAP Federation

Click:

```text
Save
```

---

# Current Result

At this point the system has:

- GPU-backed vLLM inference
- OpenAI-compatible API
- nginx reverse proxy
- HTTPS/TLS
- static bearer token auth
- LDAP identity infrastructure
- Keycloak SSO platform
- LDAP federation into Keycloak

---

# Future Architecture

Next steps:

```text
User / OpenWebUI
        ↓
oauth2-proxy
        ↓
Keycloak
        ↓
LDAP
        ↓
NGINX
        ↓
vLLM
```

This would replace:

```text
tokens.map
```

with:
- JWT validation
- SSO
- enterprise identity flows
- OAuth2/OIDC
- role-based access
- centralized authentication

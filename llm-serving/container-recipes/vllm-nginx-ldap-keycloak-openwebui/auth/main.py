from fastapi import FastAPI, Header, HTTPException
from jwt import PyJWKClient
import jwt

app = FastAPI()

ISSUER = "http://localhost:8081/realms/llm-demo"

JWKS_URL = (
"http://keycloak:8080/realms/llm-demo/"
"protocol/openid-connect/certs"
)

jwks_client = PyJWKClient(JWKS_URL)

@app.get("/validate")
def validate(authorization: str | None = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401)

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)

    token = authorization.removeprefix("Bearer ").strip()

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=ISSUER,
            options={
                "verify_aud": False,
            },
        )

        return {"ok": True}

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )

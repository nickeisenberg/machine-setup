podman run \
    --name nginx \
    --network llm-net \
    --replace \
    -p 8001:8001 \
    -v $(pwd)/nginx/nginx.conf:/etc/nginx/nginx.conf:ro,Z \
    -v $(pwd)/nginx/tokens.map:/etc/nginx/tokens.map:ro,Z \
    docker.io/library/nginx:latest

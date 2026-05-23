podman run -d \
    --name nginx \
    --network llm-net \
    -p 80:80 \
    -v $(pwd)/nginx/nginx.conf:/etc/nginx/nginx.conf:ro,Z \
    -v $(pwd)/nginx/tokens.map:/etc/nginx/tokens.map:ro,Z \
    docker.io/library/nginx:latest

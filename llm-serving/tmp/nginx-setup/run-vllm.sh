podman run \
    --name vllm \
    --network llm-net \
    --device nvidia.com/gpu=all \
    --ipc=host \
    -v ${HOME}/.local/share/huggingface/models:/models:Z \
    docker.io/vllm/vllm-openai:latest \
    --model /models/gemma-3-1b-it \
    --served-model-name gemma-3-1b-it \
    --host 0.0.0.0 \
    --port 8000 \
    --max-model-len 20000


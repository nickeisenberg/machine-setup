podman run \
  --name vllm \
  --device nvidia.com/gpu=all \
  --ipc=host \
  -p 8000:8000 \
  -v /home/nicholas/models:/models:Z \
  docker.io/vllm/vllm-openai:latest \
    --model /models/gemma-3-1b-it \
    --served-model-name gemma-3-1b-it \
    --host 0.0.0.0 \
    --port 8000 \
    --max-model-len 4000 \
    --max-num-seqs 4 \
    --gpu-memory-utilization 0.85


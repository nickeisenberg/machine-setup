MODEL_DIR=${HOME}/llm-weights
MODEL_NAME="gemma-3-270m-it"

podman run \
    --name vllm \
    --network llm-net \
    --device nvidia.com/gpu=all \
    --ipc=host \
    --replace \
    -e PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
    -v ${MODEL_DIR}:/models:Z \
    docker.io/vllm/vllm-openai:latest \
    /models/${MODEL_NAME} \
    --served-model-name ${MODEL_NAME} \
    --host 0.0.0.0 \
    --port 8000 \
    --max-model-len 2048 \
    --max-num-seqs 32 \
    --gpu-memory-utilization 0.80 \
    --enforce-eager

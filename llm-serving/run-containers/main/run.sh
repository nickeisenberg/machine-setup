export LLM_WEIGHTS_DIR="${HOME}/llm-weights"
export LLM_MODEL_NAME="gemma-3-270m-it"

podman compose up --build

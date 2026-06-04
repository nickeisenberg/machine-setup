export LLM_WEIGHTS_DIR="${HOME}/llm-weights"
export LLM_MODEL_NAME="gemma-3-270m-it"

mkdir -p \
    ./mnt/keycloak/data \
    ./mnt/ldap/config \
    ./mnt/ldap/data \

if [ ! -d "${LLM_WEIGHTS_DIR}/${LLM_MODEL_NAME}" ]; then
    echo "ERROR: Model directory not found:"
    echo "  ${LLM_WEIGHTS_DIR}/${LLM_MODEL_NAME}"
    exit 1
fi

podman compose up --build

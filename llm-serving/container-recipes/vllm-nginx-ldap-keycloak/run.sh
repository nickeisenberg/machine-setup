#!/usr/bin/env bash

set -euo pipefail

export LLM_WEIGHTS_DIR="/opt/data/shared/model-weights"
export LLM_MODEL_NAME="nvidia/Llama-4-Scout-17B-16E-Instruct-NVFP4"

# 1. Create the persistent volume directories on the host
mkdir -p \
    ./mnt/keycloak/data \
    ./mnt/ldap/config \
    ./mnt/ldap/data

# 2. Check that the LLM weights are available
if [ ! -d "${LLM_WEIGHTS_DIR}/${LLM_MODEL_NAME}" ]; then
    echo "ERROR: Model directory not found:"
    echo "  ${LLM_WEIGHTS_DIR}/${LLM_MODEL_NAME}"
    exit 1
fi

# 3. Clean up any stale container assets
podman rm --all || true

# 4. Build the vLLM and Auth container images with your host's JFrog secrets
echo "Building vLLM image with host secrets..."
podman build --secret id=pip_conf,src=$HOME/.config/pip/pip.conf \
             --secret id=jfrog_cert,src=/home/eisenbnt_la/.certificates/jfrog_nts_ops.crt \
             -t vllm-openai-fips:latest ./vllm

echo "Building Auth image with host secrets..."
podman build --secret id=pip_conf,src=$HOME/.config/pip/pip.conf \
             --secret id=jfrog_cert,src=/home/eisenbnt_la/.certificates/jfrog_nts_ops.crt \
             -t auth-fips:latest ./auth

# 5. Start the stack using the pre-built images
echo "Starting the services..."
podman compose up

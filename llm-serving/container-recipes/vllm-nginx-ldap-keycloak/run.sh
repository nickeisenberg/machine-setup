#!/usr/bin/env bash

set -euo pipefail

if [[ -z ${KEYCLOAK_ADMIN} ]] | [[ -z ${KEYCLOAK_ADMIN_PASSWORD} ]]; then
	echo "set keycloak admin and pass"
	return 1
fi

if [[ -z ${LDAP_ADMIN_PASSWORD} ]]; then
	echo "set keycloak admin and pass"
	return 1
fi

export LLM_WEIGHTS_DIR="/opt/data/shared/model-weights"
export LLM_MODEL_NAME="nvidia/Llama-4-Scout-17B-16E-Instruct-NVFP4"

mkdir -p \
    ./mnt/keycloak/data \
    ./mnt/ldap/config \
    ./mnt/ldap/data

if [ ! -d "${LLM_WEIGHTS_DIR}/${LLM_MODEL_NAME}" ]; then
    echo "ERROR: Model directory not found:"
    echo "  ${LLM_WEIGHTS_DIR}/${LLM_MODEL_NAME}"
    exit 1
fi

podman rm --all || true

# Build the vLLM and Auth container images with your host's JFrog secrets
# vllm needs rebuilding to account for fips mode enabled
echo "Building vLLM image with host secrets..."
podman build --secret id=pip_conf,src=$HOME/.config/pip/pip.conf \
             --secret id=jfrog_cert,src=/home/eisenbnt_la/.certificates/jfrog_nts_ops.crt \
             -t vllm-openai-fips:latest ./vllm

echo "Building Auth image with host secrets..."
podman build --secret id=pip_conf,src=$HOME/.config/pip/pip.conf \
             --secret id=jfrog_cert,src=/home/eisenbnt_la/.certificates/jfrog_nts_ops.crt \
             -t auth-fips:latest ./auth

echo "Starting the services..."
podman compose up

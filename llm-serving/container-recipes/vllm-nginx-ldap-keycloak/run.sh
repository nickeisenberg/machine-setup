#!/usr/bin/env bash

set -euo pipefail

export PIP_DOT_CONF="${HOME}/.config/pip/pip.conf"
export JFROG_CERTS="/home/$(whoami)/.certificates/jfrog_nts_ops.crt"

export LLM_WEIGHTS_DIR="/home/nicholas/llm-weights"
export LLM_MODEL_NAME="gemma-3-270m-it"
export NGINX_PORT="8001"

export KEYCLOAK_ADMIN="admin"
export KEYCLOAK_ADMIN_PASSWORD="adminpassword"
export KC_HOSTNAME="localhost"
export KC_HOSTNAME_PORT="8081"

export LDAP_ADMIN_PASSWORD="adminpassword"
export LDAP_PORT="1389"

if [[ -z ${KEYCLOAK_CLIENT_SECRET:-} ]]; then
	echo "WARNING: KEYCLOAK_CLIENT_SECRET has not been set."
fi

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
podman build --secret id=pip_conf,src=${PIP_DOT_CONF} \
             --secret id=jfrog_cert,src=${JFROG_CERTS} \
             -t vllm-openai-fips:latest ./vllm

echo "Building Auth image with host secrets..."
podman build --secret id=pip_conf,src=${PIP_DOT_CONF} \
             --secret id=jfrog_cert,src=${JFROG_CERTS} \
             -t auth-fips:latest ./auth

echo "Starting the services..."
podman compose up

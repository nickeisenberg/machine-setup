#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/lib/save-image.sh"

save_podman_image \
    --image docker.io/vllm/vllm-openai:latest \
    --tar-name vllm-openai.tar \
    "$@"

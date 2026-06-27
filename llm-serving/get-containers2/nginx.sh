#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/lib/save-image.sh"

save_podman_image \
    --image docker.io/library/nginx:latest \
    --tar-name nginx.tar \
    "$@"


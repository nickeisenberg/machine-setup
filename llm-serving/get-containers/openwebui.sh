#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/lib/save-image.sh"


save_podman_image \
    --image ghcr.io/open-webui/open-webui:main \
    --tar-name openwebui.tar \
    "$@"

save_podman_image \
    --image ghcr.io/open-webui/pipelines:main \
    --tar-name pipelines.tar \
    "$@"

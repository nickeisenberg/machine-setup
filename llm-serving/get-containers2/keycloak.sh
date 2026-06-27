#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/lib/save-image.sh"

save_podman_image \
    --image quay.io/keycloak/keycloak:latest \
    --tar-name keycloak.tar \
    "$@"

	


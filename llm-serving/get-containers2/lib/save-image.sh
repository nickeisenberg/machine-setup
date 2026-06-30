#!/usr/bin/env bash
set -euo pipefail

save_podman_image() {
    local image=""
    local tar_name=""
    local repull=false
    local overwrite=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --image)
                image="$2"
                shift 2
                ;;
            --tar-name)
                tar_name="$2"
                shift 2
                ;;
            --repull)
                repull=true
                shift
                ;;
            --overwrite)
                overwrite=true
                shift
                ;;
            *)
                echo "Unknown option: $1"
                return 1
                ;;
        esac
    done

	# hardcoding the save root for now.
    local save_root="/opt/data/shared/podman-images"

	if [[ ! -d ${save_root} ]]; then
		echo "${save_root} does not exist"
		return 1
	fi

    if [[ -z "${image}" ]]; then
        echo "--image is required"
        return 1
    fi

    if [[ -z "${tar_name}" ]]; then
		tar_name=$(echo ${image} | tr "/" "-")
        echo "tar_name is set to ${tar_name}"
    fi

    local image_path="${save_root}/${tar_name}"

    if [[ "${repull}" == "true" ]]; then
        echo "Force re-pulling image:"
        echo "  ${image}"
        podman pull "${image}"
    elif ! podman image exists "${image}"; then
        echo "Image not found locally. Pulling:"
        echo "  ${image}"
        podman pull "${image}"
    else
        echo "Image already exists locally:"
        echo "  ${image}"
    fi

    echo
    echo "Saving image to:"
    echo "  ${image_path}"

	if [[ -f "${image_path}" ]]; then
	    if [[ "${overwrite}" == "true" ]]; then
	        echo "Removing existing archive:"
	        echo "  ${image_path}"
	        rm -f "${image_path}"
	    else
	        echo "Error: archive already exists and overwrite is set to false:"
	        echo "  ${image_path}"
	        return 1
	    fi
	fi

    podman save -o "${image_path}" "${image}"

    echo
    echo "Done."
    echo "Load with:"
    echo "  podman load -i ${image_path}"
}

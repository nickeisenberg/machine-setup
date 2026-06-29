FROM docker.io/vllm/vllm-openai:latest

# 1. Uninstall pre-compiled wheels that bundle bad OpenSSL builds (like opencv)
RUN pip uninstall -y opencv-python-headless opencv-python

# 2. Reinstall opencv by mounting your host's pip.conf and SSL certificate 
# so the build can authenticate through your internal JFrog Artifactory proxy.
# We use $(nproc) to dynamically use all available CPU cores to speed up compilation.
RUN --mount=type=secret,id=pip_conf,target=/etc/pip.conf \
    --mount=type=secret,id=jfrog_cert,target=/home/eisenbnt_la/.certificates/jfrog_nts_ops.crt \
    MAKEFLAGS="-j$(nproc)" CMAKE_BUILD_PARALLEL_LEVEL="$(nproc)" \
    pip install --no-binary opencv-python-headless opencv-python-headless

# 3. Bake FIPS-safe environment variables directly into the image
ENV VLLM_USE_FLASHINFER_MOE_FP8=1
ENV VLLM_MM_HASHER_ALGORITHM=sha256

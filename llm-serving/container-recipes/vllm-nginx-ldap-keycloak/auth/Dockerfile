# a workout around for creating a python3.12-slim images on NTSOPs

FROM docker.io/library/alpine:3.20

RUN --mount=type=secret,id=jfrog_cert,target=/tmp/jfrog_nts_ops.crt \
    apk add \
		--no-cache ca-certificates \
		--repository=http://dl-cdn.alpinelinux.org/alpine/v3.20/main/ && \
    cat /tmp/jfrog_nts_ops.crt >> /etc/ssl/certs/ca-certificates.crt && \
    apk add --no-cache \
    	python3 \
    	py3-pip \
    	gcc \
    	musl-dev \
    	libffi-dev \
    	openssl-dev \
    	python3-dev

WORKDIR /app

RUN --mount=type=secret,id=pip_conf,target=/etc/pip.conf \
    --mount=type=secret,id=jfrog_cert,target=/home/eisenbnt_la/.certificates/jfrog_nts_ops.crt \
    pip install \
		--break-system-packages \
		--no-cache-dir \
			fastapi \
			uvicorn \
			pyjwt \
			cryptography \
			requests

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

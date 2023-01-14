FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

RUN apt-get update -y \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gcc \
    g++ \
    python3.9 \
    python3-pip \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.9 get-pip.py \
    && apt-get purge -y g++ gcc curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir \
    spacy \
    spacy-lookups-data \
    spacy-transformers \
	cupy-cuda11x \
    wandb

ENTRYPOINT ["./spacy/run_sweeps.sh"]

COPY . /spacy

RUN mkdir -p /spacy/models

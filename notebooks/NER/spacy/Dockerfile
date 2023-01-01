FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ENV CUDA_HOME=/usr/local/cuda \
    CUDA_PATH=/usr/local/cuda \
    LD_LIBRARY_PATH=$CUDA_HOME/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}} \
    PATH=$CUDA_HOME/bin${PATH:+:${PATH}}$

RUN apt-get update -y \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gcc \
    g++ \
    python3.9 \
    python3-pip \
    git \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.9 get-pip.py \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Vosloo/evaluating-student-writing.git

WORKDIR /evaluating-student-writing

RUN git checkout flair_custom_tags

RUN pip install --no-cache-dir \
    pandas \
    numpy \
    spacy \
    spacy-lookups-data \
    spacy-transformers \
	cupy-cuda11x \
    wandb \
    flair \
    scikit-learn \
    ipykernel \
    nbconvert

RUN tar xf data/dataset.tar.xz -C data \
    && ./export_path.sh \
    && jupyter nbconvert --execute --to notebook --inplace notebooks/NER/flair/column_corpus_generator.ipynb

WORKDIR notebooks/NER

RUN mkdir -p spacy/data \
    && python3.9 -m spacy convert -c ner flair/data/NER_train.txt spacy/data \
    && python3.9 -m spacy convert -c ner flair/data/NER_dev.txt spacy/data \
    && python3.9 -m spacy convert -c ner flair/data/NER_test.txt spacy/data

ENTRYPOINT python3.9 -m spacy train spacy/configs/config.cfg --verbose --output spacy/models/spacy_sweeps_1 --gpu-id 0

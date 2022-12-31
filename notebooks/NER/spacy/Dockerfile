FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip git

RUN git clone https://github.com/Vosloo/evaluating-student-writing.git

WORKDIR /evaluating-student-writing

RUN git checkout flair_custom_tags

RUN pip3 install spacy \
    spacy-lookups-data \
    cupy wanndb \
    flair \
    scikit-learn \
    ipykernel \
    nbconvert

RUN ./export_path.sh

RUN jupyter nbconvert --execute --to notebook --inplace notebooks/NER/flair/column_corpus_generator.ipynb

WORKDIR notebooks/NER

RUN python -m spacy convert -c ner flair/data/NER_train.txt spacy/data \
    python -m spacy convert -c ner flair/data/NER_dev.txt spacy/data \
    python -m spacy convert -c ner flair/data/NER_test.txt spacy/data

RUN python -m spacy train spacy/configs/config.cfg --verbose --output spacy/models/spacy_sweeps_1 --gpu-id 0

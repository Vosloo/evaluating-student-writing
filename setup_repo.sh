#!/bin/bash

# Dataset
tar xf data/dataset.tar.xz -C data

# Pretrained pipeline models
python -m spacy download en_core_web_trf

# Hooks
pre-commit autoupdate
pre-commit install

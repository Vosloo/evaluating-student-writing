#!/bin/bash

# Run sweeps
wandb sweep spacy/configs/sweep.yml &> sweep_id.txt

# Extract sweep id from sweep_id.txt
sweep_id=$(cat sweep_id.txt | grep -Po '(?<=ID: )[a-z0-9]+')

echo $(cat sweep_id.txt)

# Run sweep agent
wandb agent "evaluating-student-writing/discourse-ner/$sweep_id"

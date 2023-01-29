## Run training from this directory.
## Models should be saved into used library's models directory.
## `wandb` directory is created by wandb (duh) and is there to keep track of all runs.

---
# Flair

To run training for flair please look into **flair/train.py** file. Please adjust constants in the file to your needs, especially the `RUN_NAME` constant which is used to name the run in wandb.

---
# Spacy

Firstly you need to create IOB data format for the dataset.
To do that please execute the **flair/column_corpus_generator.ipynb** notebook.
After that you have to convert the data (from **flair/data**) to spacy format and include it in **spacy/data** directory (**You must create the directory manually if it does not exist**). To do so please execute the following commands:

```
python -m spacy convert -c ner flair/data/NER_train.txt spacy/data
python -m spacy convert -c ner flair/data/NER_dev.txt spacy/data
python -m spacy convert -c ner flair/data/NER_test.txt spacy/data
```

If the **spacy/configs/config.cfg** file is not present you can generate it from **spacy/configs/base_config.cfg** file by executing the following command:

```
python -m spacy init fill-config spacy/configs/base_config.cfg spacy/configs/config.cfg
```

If you want to send output to wandb please modify the [training.logger] section in **spacy/config.cfg** with:

```
[training.logger]
@loggers = "spacy.WandbLogger.v4"
project_name = "discourse-ner"
entity = "evaluating-student-writing"
```

To run the training process execute the following command (please adjust the `MODEL_NAME` in output parameter):

 - If you want to run the training on GPU please add `--gpu-id 0` parameter at the end
 - If you want to name your run please set env variable WANDB_NAME (if present the run will be named according to the variable)

```
python -m spacy train spacy/configs/config.cfg --verbose --output spacy/models/MODEL_NAME
```

To run the evaluation on the test set please run the following command (please adjust path to model):

(Also please note that if you want to use GPU you have to add `--gpu-id 0`)

```
python -m spacy evaluate /path/to/model data/NER_test.spacy --output data/test_metrics_output.json --displacy-path data --displacy-limit 10
```
---

## Docker

Spacy directory also includes Dockerfile created for GPU that can be built with:

```
docker build -t '<TAG_OF_THE_IMAGE>' .
```

To run the image you can use:

```
docker run --rm --gpus all -e WANDB_API_KEY='<YOUR_API_KEY>' -e WANDB_NAME='<YOUR_RUN_NAME>' <YOUR_IMAGE_TAG>:latest
```

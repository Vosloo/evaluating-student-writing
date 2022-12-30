## Run training from this directory.
## Models should be saved into used library's models directory.
## `wandb` directory is created by wandb (duh) and is there to keep track of all runs.

---
# Flair

To run training for flair please look into **flair/train.py** file. Please adjust constants in the file to your needs, especially the `RUN_NAME` constant which is used to name the run in wandb.

---
# Spacy

Firstly you need to convert IOB data format from **flair/data** to spacy format and include it in **spacy/data** directory. To do so please execute the following commands:

```
python -m spacy convert -c ner flair/data/NER_train.txt spacy/data
python -m spacy convert -c ner flair/data/NER_dev.txt spacy/data
python -m spacy convert -c ner flair/data/NER_test.txt spacy/data
```

If the **spacy/config.cfg** file is not present you can generate it from **spacy/base_config.cfg** file by executing the following command:

```
python -m spacy init fill-config spacy/base_config.cfg spacy/config.cfg
```

If you want to send output to wandb please modify the [training.logger] section in **spacy/config.cfg** with:

**(Please remember to change <#NAME_OF_RUN#> parameter to the name of your run)**

```
[training.logger]
@loggers = "spacy.WandbLogger.v4"
project_name = "discourse-ner"
entity = "evaluating-student-writing"
run_name = "<#NAME_OF_RUN#>"
```

To run the training process execute the following command (please adjust the `MODEL_NAME` in output parameter):

(If you want to run the training on GPU please add `--gpu-id 0` parameter at the end)

```
python -m spacy train spacy/config.cfg --verbose --output spacy/models/MODEL_NAME
```

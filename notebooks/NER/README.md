## Models should be saved into used library's models directory.
## `wandb` directory is created by wandb (duh) and is there to keep track of all runs.

---
For **spacy** only:<br>
If you want to send output to wandb please modify the [training.logger] section with:

```
[training.logger]
@loggers = "spacy.WandbLogger.v4"
project_name = "discourse-ner" # Project name in wandb
entity = "evaluating-student-writing" # Entity name in wandb
run_name = "<NAME_OF_RUN>"
```

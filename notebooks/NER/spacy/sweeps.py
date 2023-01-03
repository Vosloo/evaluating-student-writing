from pathlib import Path

import spacy
import typer
import wandb
from spacy import util
from spacy.training.initialize import init_nlp
from spacy.training.loop import train
from thinc.api import Config

spacy.require_gpu()

PROJECT = "discourse-ner"
ENTITY = "evaluating-student-writing"


def main(default_config: Path, output_path: Path) -> None:
    loaded_local_config = util.load_config(default_config)
    with wandb.init(project=PROJECT, entity=ENTITY) as run:  # type: ignore
        sweeps_config = Config(util.dot_to_dict(run.config))
        merged_config = Config(loaded_local_config).merge(sweeps_config)
        nlp = init_nlp(merged_config)
        train(nlp, output_path, use_gpu=True)


if __name__ == "__main__":
    typer.run(main)

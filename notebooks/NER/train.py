import sys
from pathlib import Path

module_path = Path.cwd().parent.parent
if module_path not in sys.path:
    sys.path.append(str(module_path))

import torch  # noqa: E402
import wandb  # noqa: E402
from flair.data import Corpus, Sentence  # noqa: E402
from flair.datasets import ColumnCorpus  # noqa: E402
from flair.embeddings import (  # noqa: E402 F401
    FlairEmbeddings,
    StackedEmbeddings,
    TransformerWordEmbeddings,
    WordEmbeddings,
)
from flair.models import SequenceTagger  # noqa: E402
from flair.trainers import ModelTrainer  # noqa: E402

from src.loader import TextLoader  # noqa: E402
from src.model import DatasetType  # noqa: E402

wandb.init(project="discourse-ner-test", entity="evaluating-student-writing")
wandb.config = {
    "learning_rate": 0.01,
    "mini_batch_size": 128,
    "max_epochs": 40,
}

loader = TextLoader(DatasetType.V1_WITH_PREDICTIONSTRING)

columns = {0: "text", 1: "ner"}
corpus: Corpus = ColumnCorpus(
    "data/",
    columns,
    train_file="NER_train.txt",
    dev_file="NER_dev.txt",
    test_file="NER_test.txt",
    column_delimiter=" ",
    document_separator_token="<DOC>",
    in_memory=True,
)
corpus.filter_empty_sentences()


label_dict = corpus.make_label_dictionary(label_type="ner")

embedding_types = [
    # GloVe embeddings>
    WordEmbeddings("glove"),
    # contextual string embeddings, forward
    # FlairEmbeddings('news-forward'),
    # contextual string embeddings, backward
    # FlairEmbeddings('news-backward'),
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

tagger = SequenceTagger(
    hidden_size=256,
    embeddings=embeddings,
    tag_dictionary=label_dict,
    tag_type="ner",
    use_crf=True,
)

wandb.watch(tagger)


torch.cuda.empty_cache()

trainer = ModelTrainer(tagger, corpus)

checkpoint = "models/checkpoint.pt"
if Path(checkpoint).exists():
    tagger = SequenceTagger.load(checkpoint)
    trainer.resume(
        tagger,
        base_path="models/",
        max_epochs=40,
    )
else:
    trainer.train(
        "models/",
        learning_rate=0.01,
        mini_batch_size=128,
        max_epochs=40,
        patience=4,
        anneal_factor=0.9,
        num_workers=8,
        main_evaluation_metric=("weighted avg", "f1-score"),
        monitor_train=True,
        write_weights=True,
        create_file_logs=True,
        create_loss_file=True,
        optimizer=torch.optim.Adam,
        checkpoint=True,
        shuffle=True,
        embeddings_storage_mode="gpu",
        train_with_dev=False,
    )

model = SequenceTagger.load("models/final-model.pt")

text = loader.load_random_text()

sent = Sentence(text.text)
model.predict(sent)

for disc in text.discourses:
    print(disc)

print()
print(sent.to_tagged_string())

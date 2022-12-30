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
    ELMoEmbeddings,
    FastTextEmbeddings,
    WordEmbeddings,
)
from flair.models import SequenceTagger  # noqa: E402
from flair.trainers import ModelTrainer  # noqa: E402

from src.loader import TextLoader  # noqa: E402
from src.model import DatasetType  # noqa: E402

MODELS_DIR = "models/"
DATA_DIR = "data/"

RUN_NAME = "flair-ner"
LR = 0.1
MINI_BATCH_SIZE = 128
MAX_EPOCHS = 40

wandb.init(project="discourse-ner", entity="evaluating-student-writing", name=RUN_NAME)
wandb.config = {
    "learning_rate": LR,
    "mini_batch_size": MINI_BATCH_SIZE,
    "max_epochs": MAX_EPOCHS,
}

loader = TextLoader(DatasetType.V1_WITH_PREDICTIONSTRING)

columns = {0: "text", 1: "ner"}
corpus: Corpus = ColumnCorpus(
    DATA_DIR,
    columns,
    train_file="NER_train.txt",
    dev_file="NER_dev.txt",
    test_file="NER_test.txt",
    column_delimiter=" ",
    document_separator_token="-DOCSTART- -X- O O",
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
trainer.train(
    MODELS_DIR,
    learning_rate=LR,
    mini_batch_size=MINI_BATCH_SIZE,
    max_epochs=MAX_EPOCHS,
    patience=4,
    anneal_factor=0.7,
    num_workers=8,
    main_evaluation_metric=("weighted avg", "f1-score"),
    monitor_train=False,
    write_weights=True,
    create_file_logs=True,
    create_loss_file=True,
    optimizer=torch.optim.Adam,
    checkpoint=True,
    embeddings_storage_mode="gpu",
    shuffle=True,
    train_with_dev=False,
)

model = SequenceTagger.load(MODELS_DIR + "final-model.pt")

text = loader.load_random_text()

sent = Sentence(text.text)
model.predict(sent)

for disc in text.discourses:
    print(disc)

print()
print(sent.to_tagged_string())

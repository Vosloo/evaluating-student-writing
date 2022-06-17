import pandas as pd

from src.discourse import Discourse
from src.text import Text


DISCOURSE_ID = "discourse_id"
DISCOURSE_START = "discourse_start"
DISCOURSE_END = "discourse_end"
DISCOURSE_TEXT = "discourse_text"
DISCOURSE_TYPE = "discourse_type"


class TextLoader:
    DATASET_PATH = "data/dataset"
    TRAIN_DIR = DATASET_PATH + "/train"
    TEST_DIR = DATASET_PATH + "/test"
    TRAIN_CSV = DATASET_PATH + "/train.csv"

    def __init__(self) -> None:
        self.train_df = pd.read_csv(self.TRAIN_CSV).astype(
            {DISCOURSE_ID: int, DISCOURSE_START: int, DISCOURSE_END: int}
        )

    def load_text_with_id(self, text_id: str) -> Text:
        with open(self.TRAIN_DIR + "/" + text_id + ".txt", "r") as f:
            text = f.read()

        discourses_df = self.train_df.loc[self.train_df["id"] == text_id].reset_index(drop=True)

        discourses = []
        for row in discourses_df.itertuples():
            discourse = Discourse(
                row.discourse_id,
                row.discourse_start,
                row.discourse_end,
                row.discourse_text,
                row.discourse_type,
            )
            discourses.append(discourse)

        return Text(text_id, text, discourses)


if __name__ == "__main__":
    text_loader = TextLoader()
    text = text_loader.load_text_with_id("423A1CA112E2")
    print(repr(text))

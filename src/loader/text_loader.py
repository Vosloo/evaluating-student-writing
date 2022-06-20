from typing import Generator

import pandas as pd
from src.loader import Discourse, Text
from src.purifier import Purifier

ID = "id"

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

        self.unique_ids = self.train_df[ID].unique()

    def __iter__(self) -> Generator[Text, None, None]:
        for text_id in self.unique_ids:
            yield self.load_text_with_id(text_id)

    def __len__(self) -> int:
        return len(self.unique_ids)

    def load_text_with_id(self, text_id: str, purify_discourses: bool = False) -> Text:
        with open(self.TRAIN_DIR + "/" + text_id + ".txt", "r") as f:
            text = f.read()

        discourses_df: pd.DataFrame = self.train_df.loc[self.train_df[ID] == text_id].reset_index(
            drop=True
        )
        if purify_discourses:
            discourses_df.loc[:, DISCOURSE_TEXT] = discourses_df[DISCOURSE_TEXT].apply(
                Purifier.purify_text
            )

        discourses = []
        for row in discourses_df.itertuples():
            discourse = Discourse(
                row.discourse_id,  # type: ignore[attr-defined]
                row.discourse_start,  # type: ignore[attr-defined]
                row.discourse_end,  # type: ignore[attr-defined]
                row.discourse_text,  # type: ignore[attr-defined]
                row.discourse_type,  # type: ignore[attr-defined]
            )
            discourses.append(discourse)

        return Text(text_id, text, discourses)


if __name__ == "__main__":
    text_loader = TextLoader()

    counter = 0
    for text in text_loader:
        if counter == 10:
            break

        print(text)
        counter += 1

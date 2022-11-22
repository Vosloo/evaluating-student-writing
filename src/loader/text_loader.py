from typing import Generator

import numpy as np
import pandas as pd
from definitions import ROOT_DIR
from src.model import Discourse, Text, DiscourseType
from src.purifier import Purifier

ID = "id"

DISCOURSE_ID = "discourse_id"
DISCOURSE_START = "discourse_start"
DISCOURSE_END = "discourse_end"
DISCOURSE_TEXT = "discourse_text"
DISCOURSE_TYPE = "discourse_type"


class TextLoader:
    DATASET_PATH = ROOT_DIR + "/data/dataset"
    TRAIN_DIR = DATASET_PATH + "/train"
    TEST_DIR = DATASET_PATH + "/test"
    TRAIN_CSV = DATASET_PATH + "/train.csv"

    def __init__(self) -> None:
        self._df = pd.read_csv(self.TRAIN_CSV).astype(
            {DISCOURSE_ID: np.int64, DISCOURSE_START: np.int64, DISCOURSE_END: np.int64}
        )

        self.unique_ids = np.array(self._df[ID].unique())
        self.purifier: Purifier = Purifier()

    def __iter__(self) -> Generator[str, None, None]:
        for ind, text_id in enumerate(self.unique_ids):
            print(f"\r{ind + 1:4} / {len(self.unique_ids):4}", end="")
            if ind + 1 == len(self.unique_ids):
                print()

            yield text_id

    def __len__(self) -> int:
        return len(self.unique_ids)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def load_text_with_id(
        self, text_id: str, purify_discourses: bool = False, purify_text: bool = False
    ) -> Text:
        with open(self.TRAIN_DIR + "/" + text_id + ".txt", "r", encoding="utf-8") as f:
            text = f.read()

        if purify_text:
            text = self.purifier.purify(text)

        discourses_df: pd.DataFrame = self._df.loc[self._df[ID] == text_id].reset_index(drop=True)
        if purify_discourses:
            discourses_df.loc[:, DISCOURSE_TEXT] = discourses_df[DISCOURSE_TEXT].apply(
                self.purifier.purify
            )

        discourses = []
        for row in discourses_df.itertuples():
            discourse = Discourse(
                row.discourse_id,  # type: ignore[attr-defined]
                row.discourse_start,  # type: ignore[attr-defined]
                row.discourse_end,  # type: ignore[attr-defined]
                row.discourse_text,  # type: ignore[attr-defined]
                DiscourseType(row.discourse_type),  # type: ignore[attr-defined]
                row.predictionstring,  # type: ignore[attr-defined]
            )
            discourses.append(discourse)

        return Text(text_id, text, discourses)

    def load_random_text(self, purify_discourses: bool = False) -> Text:
        text_id = np.random.choice(self.unique_ids)

        return self.load_text_with_id(text_id, purify_discourses)

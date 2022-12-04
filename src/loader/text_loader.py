from typing import Generator, Union

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
        self.unique_ids_shuffled: Union[np.ndarray, None] = None
        self.purifier: Purifier = Purifier()

    def __iter__(self) -> Generator[str, None, None]:
        for text_id in self.unique_ids:
            yield text_id

    def __len__(self) -> int:
        return len(self.unique_ids)

    def _get_shuffled(self, seed: Union[int, None] = None) -> np.ndarray:
        if self.unique_ids_shuffled is None:
            if seed is not None:
                np.random.seed(seed)

            self.unique_ids_shuffled = np.random.choice(
                self.unique_ids, len(self.unique_ids), replace=False
            )

        return self.unique_ids_shuffled

    def _fix_predictionstring(
        self, text: str, disc_start: int, disc_end: int, predictionstring: str
    ) -> str:
        # TODO
        text[disc_start:disc_end].split()
        # pred_start, pred_end = int(predictionstring[0]), int(predictionstring[-1])
        text.split()
        return ""

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def iterate(
        self, offset: int = 0, limit: int = 0, shuffle: bool = False, seed: Union[int, None] = None
    ) -> Generator[Text, None, None]:
        """
        Iterate over the texts in the dataset.

        :param offset: The offset to start iterating from (based on texts' unique ids).
        :param limit: The maximum number of texts to iterate over.
        :param shuffle: Whether to shuffle the texts before iterating.
        :param seed: The seed to use for shuffling (if shuffle is True).

        :return: A generator that yields the text object.
        """
        if limit == 0:
            limit = len(self.unique_ids)

        if shuffle:
            unique_ids_shuffled = self._get_shuffled(seed)
            ids = unique_ids_shuffled[offset : offset + limit]
        else:
            ids = self.unique_ids[offset : offset + limit]

        for text_id in ids:
            yield self.load_text_with_id(text_id)

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

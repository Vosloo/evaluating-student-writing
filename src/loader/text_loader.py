from typing import Union, Iterator

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

    def __iter__(self) -> Iterator[str]:
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

    # def _is_predictionstring_valid(
    #     self, text_id: int, text: str, disc_start: int, disc_end: int, predictionstring: str
    # ) -> tuple[bool, str]:
    #     disc_words = text[disc_start:disc_end].split()
    #     pred_idx = predictionstring.split()
    #     pred_start, pred_end = int(pred_idx[0]), int(pred_idx[-1])

    #     words = text.split()
    #     if disc_words[0] in (".", ",", "!", "?"):
    #         pred_end -= 1
    #         del disc_words[0]

    #     selected = words[pred_start : pred_end + 1]

    #     disc_words[-1] = disc_words[-1].strip(".,!?")
    #     selected[-1] = selected[-1].strip(".,!?")

    #     if disc_words != selected:
    #         print("id:", text_id)
    #         print(f"{disc_words} !=\n{selected}", end="\n\n")
    #         return False, ""

    #     return True, " ".join(range(pred_start, pred_end + 1))

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def iterate(
        self,
        offset: int = 0,
        limit: int = 0,
        shuffle: bool = False,
        seed: Union[int, None] = None,
        purify_text: bool = False,
        purify_discourses: bool = False,
        verbose: bool = False,
    ) -> Iterator[Text]:
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

        for ind, text_id in enumerate(ids):
            if verbose:
                print(f"\r{ind + 1:3} / {len(ids)}", end="")

            yield self.load_text_with_id(text_id, purify_discourses, purify_text)

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
            # (is_predictionstring_valid, predictionstring) = self._is_predictionstring_valid(
            #     text_id, text, row.discourse_start, row.discourse_end, row.predictionstring  # type: ignore[attr-defined] # noqa: E501
            # )

            discourse = Discourse(
                row.discourse_id,  # type: ignore[attr-defined]
                row.discourse_start,  # type: ignore[attr-defined]
                row.discourse_end,  # type: ignore[attr-defined]
                row.discourse_text,  # type: ignore[attr-defined]
                DiscourseType(row.discourse_type),  # type: ignore[attr-defined]
                # self._is_predictionstring_valid(
                #     text_id, text, row.discourse_start, row.discourse_end, row.predictionstring  # type: ignore[attr-defined] # noqa: E501
                # ),
                row.predictionstring,  # type: ignore[attr-defined]
            )
            discourses.append(discourse)

        return Text(text_id, text, discourses)

    def load_random_text(self, purify_discourses: bool = False) -> Text:
        text_id = np.random.choice(self.unique_ids)

        return self.load_text_with_id(text_id, purify_discourses)

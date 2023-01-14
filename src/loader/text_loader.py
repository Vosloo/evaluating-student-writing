from typing import Iterator, Union

import numpy as np
import pandas as pd

from definitions import ROOT_DIR
from src.model import DatasetType, Discourse, DiscourseType, Text
from src.purifier import Purifier

ID = "id"

DISCOURSE_ID = "discourse_id"
DISCOURSE_START = "discourse_start"
DISCOURSE_END = "discourse_end"
DISCOURSE_TEXT = "discourse_text"
DISCOURSE_TYPE = "discourse_type"

DATA_PATH = ROOT_DIR + "/data"
DATASET_PATH = DATA_PATH + "/dataset"
TRAIN_DIR = DATASET_PATH + "/train"

ORIGINAL_DATASET = DATASET_PATH + "/train.csv"
V1_NO_PREDICTIONSTRING_DATASET = DATA_PATH + "/train_v1_no_predictionstring.xz"
V1_WITH_PREDICTIONSTRING_DATASET = DATA_PATH + "/train_v1_with_predictionstring.xz"


class TextLoader:
    def __init__(self, dataset_type: DatasetType = DatasetType.V1_WITH_PREDICTIONSTRING) -> None:
        self._df = self._load_dataset(dataset_type)
        self._dataset_type = dataset_type

        self.unique_ids = np.array(self._df[ID].unique())
        self.unique_ids_shuffled: Union[np.ndarray, None] = None
        self.purifier: Purifier = Purifier()

    def __iter__(self) -> Iterator[str]:
        for text_id in self.unique_ids:
            yield text_id

    def __len__(self) -> int:
        return len(self.unique_ids)

    def _load_dataset(self, dataset_type: DatasetType) -> pd.DataFrame:
        if dataset_type == DatasetType.ORIGINAL:
            df = pd.read_csv(ORIGINAL_DATASET)
        elif dataset_type == DatasetType.V1_NO_PREDICTIONSTRING:
            df = pd.read_csv(V1_NO_PREDICTIONSTRING_DATASET, compression="xz")
        elif dataset_type == DatasetType.V1_WITH_PREDICTIONSTRING:
            df = pd.read_csv(V1_WITH_PREDICTIONSTRING_DATASET, compression="xz")
        else:
            raise ValueError(f"Unknown dataset type: {dataset_type}")

        df = df.astype({DISCOURSE_ID: np.int64, DISCOURSE_START: np.int64, DISCOURSE_END: np.int64})

        return df

    def _get_shuffled(self, seed: Union[int, None] = None) -> np.ndarray:
        if self.unique_ids_shuffled is None:
            if seed is not None:
                np.random.seed(seed)

            self.unique_ids_shuffled = np.random.choice(
                self.unique_ids, len(self.unique_ids), replace=False
            )

        return self.unique_ids_shuffled

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
        :param purify_text: Whether to purify the text.
        :param purify_discourses:
            Whether to purify the discourses. (does not apply for purified datasets)
        :param verbose: Whether to print the progress.

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
        """
        Load a text object from the dataset.

        :param text_id: The id of the text to load.
        :param purify_discourses:
            Whether to purify the discourses. (does not apply for purified datasets)
        :param purify_text: Whether to purify the text.

        :return: The text object.
        """
        with open(TRAIN_DIR + "/" + text_id + ".txt", "r", encoding="utf-8") as f:
            text = f.read()

        if purify_text:
            text = self.purifier.purify(text)

        discourses_df: pd.DataFrame = self._df.loc[self._df[ID] == text_id].reset_index(drop=True)
        if purify_discourses and self._dataset_type == DatasetType.ORIGINAL:
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

    def load_random_text(self, purify_discourses: bool = False, purify_text: bool = False) -> Text:
        """
        Load a random text object from the dataset.

        :param purify_discourses:
            Whether to purify the discourses. (does not apply for purified datasets)
        :param purify_text: Whether to purify the text.

        :return: The text object.
        """
        text_id = np.random.choice(self.unique_ids)

        return self.load_text_with_id(text_id, purify_discourses, purify_text)

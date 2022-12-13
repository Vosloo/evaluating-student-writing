from typing import Union
from .discourse import Discourse


class Text:
    def __init__(self, text_id: str, text: str, discourses: list[Discourse]) -> None:
        self.id = text_id
        self.text = text
        self.words = text.split()
        self.discourses = discourses

        parts, gap_len = self._get_non_classified_parts()
        self.non_classified_parts = parts
        self.gap_len = gap_len

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return self.id

    def __len__(self) -> int:
        return len(self.text)

    def __getitem__(self, index: int) -> str:
        return self.text[index]

    def __getslice__(self, start: int, end: int) -> str:
        return self.text[start:end]

    @property
    def info(self) -> str:
        return f"Text id: {self.id}; Length: {len(self.text)}; Discourses: {len(self.discourses)}"

    def index(self, phrase: str, start: Union[int, None] = None) -> int:
        try:
            res = self.text.index(phrase, start)
        except ValueError:
            raise ValueError(f"Phrase '{phrase}' not found for start {start} in text '{self.id}'")

        return res

    def split(self) -> list[str]:
        return self.words

    def _get_non_classified_parts(self) -> tuple[list[tuple[int, int]], int]:
        if len(self.discourses) == 0:
            return [(0, len(self) - 1)], len(self)

        non_classified_parts = []
        gap_len = 0

        curr_ind = 0
        for discourse in self.discourses:
            if discourse.ind_start > curr_ind:
                gap_len += discourse.ind_start - curr_ind
                non_classified_parts.append((curr_ind, discourse.ind_start))

            curr_ind = discourse.ind_end

        if curr_ind < len(self):
            gap_len += len(self) - curr_ind
            non_classified_parts.append((curr_ind, len(self)))

        return non_classified_parts, gap_len

from dataclasses import dataclass
from functools import cached_property

from .discourse_type import DiscourseType


@dataclass
class Discourse:
    def __init__(
        self,
        discourse_id: int,
        discourse_start: int,
        discourse_end: int,
        discourse_text: str,
        discourse_type: DiscourseType,
        predictionstring: str,
    ):
        self.id = discourse_id
        self.ind_start = discourse_start
        self.ind_end = discourse_end
        self.text = discourse_text
        self.words = discourse_text.split()
        self.type = discourse_type
        self._predictionstring = predictionstring

    def __str__(self) -> str:
        pred_start, pred_end = self.predictionstring[0], self.predictionstring[-1]
        header = (
            f"--- {self.id} ({self.ind_start} -> {self.ind_end} |"
            f" {pred_start} -> {pred_end}) - {self.type.value} ---"
        )
        return f"{header}\n{self.text}\n{'-' * len(header)}"

    def __repr__(self) -> str:
        return repr(self.__str__())

    @cached_property
    def predictionstring(self) -> list[int]:
        return list(map(int, self._predictionstring.split()))

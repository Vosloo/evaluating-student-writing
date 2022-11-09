from dataclasses import dataclass


@dataclass
class Discourse:
    def __init__(
        self,
        discourse_id: int,
        discourse_start: int,
        discourse_end: int,
        discourse_text: str,
        discourse_type: str,
    ):
        self.id = discourse_id
        self.ind_start = discourse_start
        self.ind_end = discourse_end
        self.text = discourse_text
        self.type = discourse_type

    def __str__(self) -> str:
        header = f"--- {self.id} ({self.ind_start} -> {self.ind_end}) - {self.type} ---"
        return f"{header}\n{self.text}\n{'-' * len(header)}"

    def __repr__(self) -> str:
        return repr(self.__str__())

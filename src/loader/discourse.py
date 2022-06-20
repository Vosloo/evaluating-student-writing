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
        self.discourse_id = discourse_id
        self.discourse_start = discourse_start
        self.discourse_end = discourse_end
        self.discourse_text = discourse_text
        self.discourse_type = discourse_type

    def __str__(self) -> str:
        return self.discourse_text

    def __repr__(self) -> str:
        return repr(self.__str__())

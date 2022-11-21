from .discourse import Discourse


class Text:
    def __init__(self, text_id: str, text: str, discourses: list[Discourse]) -> None:
        self.id = text_id
        self.text = text
        self.words = text.split()
        self.discourses = discourses

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

from src.loader import Discourse


class Text:
    def __init__(self, text_id: str, text: str, discourses: list[Discourse]) -> None:
        self.text_id = text_id
        self.text = text
        self.discourses = discourses

    def __str__(self) -> str:
        return f"Text id: {self.text_id}; Length: {len(self.text)}; Discourses: {len(self.discourses)}"

    def __repr__(self) -> str:
        return repr(self.__str__())

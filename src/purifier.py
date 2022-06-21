import regex as re


class Purifier:
    REGEX_MULTIPLE_NEWLINES = (r"\n{2,}", "\n")
    REGEX_NEWLINES_SENTENCES = (r"\n(.)", r" \1")
    REGEX_MULTIPLE_SPACES = (r" {2,}", " ")
    REGEX_SPACE_AFTER_CHAR = (r"(\w) ([,.])", r"\1\2")
    REGEX_SPACE_COMMA = (r",(\p{L})", r", \1")

    @staticmethod
    def purify_text(text: str) -> str:
        text = re.sub(*Purifier.REGEX_MULTIPLE_NEWLINES, text)
        text = re.sub(*Purifier.REGEX_NEWLINES_SENTENCES, text)
        text = re.sub(*Purifier.REGEX_MULTIPLE_SPACES, text)
        text = re.sub(*Purifier.REGEX_SPACE_AFTER_CHAR, text)
        text = re.sub(*Purifier.REGEX_SPACE_COMMA, text)

        return text.strip()

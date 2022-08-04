import regex as re


class Purifier:
    REGEX_ATTACHMENT_NUMBER = (r"\(\d{1,}\)", "")
    REGEX_LEAVE_LETTERS_CHARACTERS = (r"[^\p{L}\d\s\n'.]", "")
    REGEX_MULTIPLE_NEWLINES = (r"\n{2,}", "\n")
    REGEX_NEWLINES_SENTENCES = (r"\n(.)", r" \1")
    REGEX_MULTIPLE_SPACES = (r" {2,}", " ")
    REGEX_SPACE_AFTER_CHAR = (r"(\w) ([,.])", r"\1\2 ")  # a . => a.
    REGEX_SPACE_AFTER_COMMA = (
        r"(?P<pre>[^\d]),(?P<after>[^\s])|,(?P<after1>[^\d\s])",  # that,"In => that, "In
        r"\g<pre>, \g<after>\g<after1>",  # 3,477 => 3,477 (stays the same)
    )
    REGEX_SPACE_COMMA = (r",(\p{L})", r", \1")

    @staticmethod
    def purify(text: str) -> str:
        text = re.sub(*Purifier.REGEX_ATTACHMENT_NUMBER, text)
        text = re.sub(*Purifier.REGEX_LEAVE_LETTERS_CHARACTERS, text)
        text = re.sub(*Purifier.REGEX_MULTIPLE_NEWLINES, text)
        text = re.sub(*Purifier.REGEX_NEWLINES_SENTENCES, text)
        text = re.sub(*Purifier.REGEX_MULTIPLE_SPACES, text)
        text = re.sub(*Purifier.REGEX_SPACE_AFTER_CHAR, text)
        text = re.sub(*Purifier.REGEX_SPACE_AFTER_COMMA, text)
        text = re.sub(*Purifier.REGEX_SPACE_COMMA, text)
        # Again as some spaces could be addedby previous regexps
        text = re.sub(*Purifier.REGEX_MULTIPLE_SPACES, text)

        return text.strip()

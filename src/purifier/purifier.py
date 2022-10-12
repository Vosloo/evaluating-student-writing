import regex as re


class Purifier:
    REGEX_ATTACHMENT_NUMBER = (r"\(\d{1,}\)", "")  # (1), (12), etc.
    # leaves only letters, numbers, spaces, newlines, apostrophes and dots
    REGEX_LEAVE_LETTER_CHARACTERS = (r"[^\p{L}\d\s\n'.]", "")
    REGEX_MULTIPLE_NEWLINES = (r"\n{2,}", "\n")
    REGEX_NEWLINES_SENTENCES = (r"\n(.)", r" \1")
    REGEX_HEX_SPACE = (r"\xa0", " ")
    REGEX_MULTIPLE_SPACES = (r" {2,}", " ")
    REGEX_SPACE_AFTER_CHAR = (r"(\w) ([,.])", r"\1\2 ")  # a . => a.
    REGEX_SPACE_AFTER_COMMA = (
        r"(?P<pre>[^\d]),(?P<after>[^\s])|,(?P<after1>[^\d\s])",  # that,"In => that, "In
        r"\g<pre>, \g<after>\g<after1>",  # 3,477 => 3,477 (stays the same)
    )
    REGEX_LINKS = (
        r"(?:(?:(?:(?:ftp|https?):\/\/)(?:www\.)?|www)\s*.*?\.\s*\w+[\w\/\-#]*"
        r"(?:\.\w+(?:\/[\w\/#\-\.]+)?)?|\w+\.(?:org|com|html?|pl|en|net|edu|php))",
        "",
    )
    REGEX_LINKS_REMNANTS = (
        r"\(?\.?\s?(?:(?:[\w-]+\/|[\w-]+(?=\.)))*\.\s?(?:org|com|html?|pl|en|net|edu|php)\)?",
        "",
    )

    def purify(self, text: str) -> str:
        text = re.sub(*Purifier.REGEX_LINKS, text, flags=re.IGNORECASE)
        text = re.sub(*Purifier.REGEX_LINKS_REMNANTS, text, flags=re.IGNORECASE)
        text = re.sub(*Purifier.REGEX_ATTACHMENT_NUMBER, text)
        text = re.sub(*Purifier.REGEX_SPACE_AFTER_CHAR, text)
        text = re.sub(*Purifier.REGEX_SPACE_AFTER_COMMA, text)
        text = re.sub(*Purifier.REGEX_LEAVE_LETTER_CHARACTERS, text)
        text = re.sub(*Purifier.REGEX_MULTIPLE_NEWLINES, text)
        text = re.sub(*Purifier.REGEX_NEWLINES_SENTENCES, text)
        text = re.sub(*Purifier.REGEX_MULTIPLE_SPACES, text)
        text = re.sub(*Purifier.REGEX_HEX_SPACE, text)
        # Again as some spaces could be addedby previous regexps
        text = re.sub(*Purifier.REGEX_MULTIPLE_SPACES, text)

        return text.strip()

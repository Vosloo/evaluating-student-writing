import regex as re


class Purifier:
    COMMON_DOMAINS = ["org", "com", "html", "htm", "en", "net", "edu", "php", "gov", "info"]
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
    REGEX_DOT_DOMAIN = (r"\.\s*(org|com|html|htm|en|net|edu|php|gov|info)", r".\1")
    REGEX_LINKS = (
        r"\(?(?:(?:(?:(?:ftp|https?):\/\/)(?:www\.)?|www)\s*.*?\.\s*\w+[\w\/\-#]*"
        r"(?:\.\w+(?:\/[\w\/#\-\.]+)?)?|\w+\.(?:{domains}))"
        r"(?:(?:\(?\.?\s?(?:(?:[\w-]+\/|[\w-]+(?=\.)))*\.(?:{domains}))|(?=\s|\.|,|$))\)?",
        "",
    )

    def purify(self, text: str) -> str:
        text = re.sub(*Purifier.REGEX_LEAVE_LETTER_CHARACTERS, text)
        text = re.sub(*Purifier.REGEX_DOT_DOMAIN, text, flags=re.IGNORECASE)
        text = re.sub(*self._get_regex_links(), text, flags=re.IGNORECASE)
        text = re.sub(*Purifier.REGEX_ATTACHMENT_NUMBER, text)
        text = re.sub(*Purifier.REGEX_SPACE_AFTER_CHAR, text)
        text = re.sub(*Purifier.REGEX_SPACE_AFTER_COMMA, text)
        text = re.sub(*Purifier.REGEX_MULTIPLE_NEWLINES, text)
        text = re.sub(*Purifier.REGEX_NEWLINES_SENTENCES, text)
        text = re.sub(*Purifier.REGEX_MULTIPLE_SPACES, text)
        text = re.sub(*Purifier.REGEX_HEX_SPACE, text)
        # Again as some spaces could be addedby previous regexps
        text = re.sub(*Purifier.REGEX_MULTIPLE_SPACES, text)

        return text.strip()

    def _get_regex_links(self) -> tuple[str, str]:
        pattern, replacement = Purifier.REGEX_LINKS
        return pattern.format(domains="|".join(Purifier.COMMON_DOMAINS)), replacement

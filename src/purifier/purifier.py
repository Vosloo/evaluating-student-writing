import regex as re

COMMON_DOMAINS = ["org", "com", "html", "htm", "en", "uk", "net", "edu", "php", "gov", "info", "au"]


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
    REGEX_DOT_DOMAIN = (r"\.\s*({domains})(?!\w)", r".\1")
    REGEX_LINKS = (
        r"( ?(?:(?:ftp|https?):\/\/(?:www\.)|www\.|\w+@|)? ?\w+(?P<sub_domains>\.(?:{domains}))"
        r"(?P>sub_domains)*(?:[\w\/-]+)?(?P>sub_domains)?)",
        "",
    )
    REGEX_MERGED_WORDS = ("(?P<word>[A-Z]?[a-z]+)(?P<next>[A-Z][a-z]+)", r"\g<word> \g<next>")
    REGEX_DOT_AT_START = (r"^\.", "")
    REGEX_SPLIT_IF = (r"(\w)if ", r"\1 if ")

    def purify(self, text: str) -> str:
        text = re.sub(*Purifier.REGEX_LEAVE_LETTER_CHARACTERS, text)
        text = re.sub(*self._embed_domains(Purifier.REGEX_DOT_DOMAIN), text, flags=re.IGNORECASE)
        text = re.sub(*self._embed_domains(Purifier.REGEX_LINKS), text, flags=re.IGNORECASE)
        text = re.sub(*Purifier.REGEX_ATTACHMENT_NUMBER, text)
        text = re.sub(*Purifier.REGEX_MERGED_WORDS, text)
        text = re.sub(*Purifier.REGEX_SPLIT_IF, text)
        text = re.sub(*Purifier.REGEX_SPACE_AFTER_CHAR, text)
        text = re.sub(*Purifier.REGEX_SPACE_AFTER_COMMA, text)
        text = re.sub(*Purifier.REGEX_MULTIPLE_NEWLINES, text)
        text = re.sub(*Purifier.REGEX_NEWLINES_SENTENCES, text)
        text = re.sub(*Purifier.REGEX_MULTIPLE_SPACES, text)
        text = re.sub(*Purifier.REGEX_HEX_SPACE, text)
        # Again as some spaces could be addedby previous regexps
        text = re.sub(*Purifier.REGEX_MULTIPLE_SPACES, text)
        text = re.sub(*Purifier.REGEX_DOT_AT_START, text)

        return text.strip()

    def _embed_domains(self, regex_pair: tuple[str, str]) -> tuple[str, str]:
        pattern, replacement = regex_pair
        return pattern.format(domains="|".join(COMMON_DOMAINS)), replacement

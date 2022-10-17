import pytest
import regex as re
from src.loader import TextLoader
from src.model import Text
from src.purifier import Purifier

from .data_provider import get_test_cases

TYPE_TEST_CASE = tuple[list[str], Text]


@pytest.fixture
def purifier() -> Purifier:
    return Purifier()


class TestLinks:
    @pytest.mark.parametrize("test_case", get_test_cases(TextLoader()))
    def test_links(self, test_case: TYPE_TEST_CASE, purifier: Purifier) -> None:
        links, text = test_case

        pattern, _ = purifier._get_regex_links()
        dot_domains = purifier.REGEX_DOT_DOMAIN
        text = re.sub(*dot_domains, text.text)
        found_links = re.findall(pattern, text, flags=re.IGNORECASE)
        assert len(found_links) == len(links)
        for ind, link in enumerate(links):
            assert link == found_links[ind]

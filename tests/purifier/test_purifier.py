import pytest
from src.purifier import Purifier

from .data_provider import get_test_cases


class TestPurifier:
    @pytest.mark.parametrize("test_case", get_test_cases())
    def test_purifying(self, test_case: dict, purifier: Purifier) -> None:
        purified = purifier.purify(test_case["input"])

        assert purified == test_case["expected"]

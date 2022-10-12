from typing import Generator

from src.loader import TextLoader
from src.model import Text

CASES_WITH_LINKS = ["D14A82EE41BF", "E7C2FE6B860D"]
EXPECTED_MATCHES = {
    "D14A82EE41BF": [
        "https://www. netsafeutah. org/teens/staysafe/distracted_driving",
        "https://www. nhtsa. gov/risky-driving/distracted-driving",
        "https://www. abc. net",
    ],
    "E7C2FE6B860D": [
        "https://www. edgarsnyder. com/car-accident/cause-of-accident/cell-phone/cell-phone-statistics",
        "https://www. edgarsnyder. com/car-accident/cause-of-accident/cell-phone/cell-phone-statistics",
        "DMV.ORG",
        "www. dmv",
        "www. edgarsnyder",
    ],
}

TYPE_TEST_CASE = Generator[tuple[list[str], Text], None, None]


def get_test_cases(loader: TextLoader) -> TYPE_TEST_CASE:
    for text_id in CASES_WITH_LINKS:
        yield EXPECTED_MATCHES[text_id], loader.load_text_with_id(text_id)

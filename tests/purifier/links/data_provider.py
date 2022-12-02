from typing import Generator

from src.loader import TextLoader
from src.model import Text

CASES_WITH_LINKS = ["D14A82EE41BF", "D5D31918A943", "E7C2FE6B860D"]
EXPECTED_MATCHES: dict[str, list[str]] = {
    "D14A82EE41BF": [
        " https://www.netsafeutah.org/teens/staysafe/distracted_driving.html",
        " https://www. nhtsa.gov/risky-driving/distracted-driving",
        "https://www. abc.net.au/science/articles/2011/10/06/3333955.htm",
    ],
    "D5D31918A943": [
        " thezebra.com",
        " teendriversource.org",
        " ctr@dot.gov",
        " www. nhtsa.gov/risky-driving/distracted-driving",
        " fivethirtyeight.com/features/driving-your-phone-is-a-distraction-even-if-you-arent-looking-at-it/",  # noqa: E501
        " www. teendriversource.org/teen-crash-risks-prevention/distracted-driving/cell-phones",
        " www. iii.org/fact-statistic/facts-statistics-distracted-driving",
        " www. nidirect.gov.uk/articles/using-your-mobile-phone-while-driving",
    ],
    "E7C2FE6B860D": [
        "https://www. edgarsnyder.com/car-accident/cause-of-accident/cell-phone/cell-phone-statistics.html",  # noqa: E501
        "https://www. edgarsnyder.com/car-accident/cause-of-accident/cell-phone/cell-phone-statistics.html",  # noqa: E501
        " DMV.ORG",
        " www. dmv.org/distracted-driving/texting-and-driving.php",
        " Edgarsnyder.com",
        " www. edgarsnyder.com/car-accident/cause-of-accident/cell-phone/cell-phone-statistics.html",
    ],
}

TYPE_TEST_CASE = Generator[tuple[list[str], Text], None, None]


def get_test_cases(loader: TextLoader) -> TYPE_TEST_CASE:
    for text_id in CASES_WITH_LINKS:
        yield EXPECTED_MATCHES[text_id], loader.load_text_with_id(text_id)

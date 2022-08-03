import pytest
from src.loader import TextLoader


TRAIN_DIR = "data/dataset/train/"
TEST_ID = "AB741655902E"
NO_DISCOURSES = 6


class TestTextLoader:
    def test_load_specific_id(self, expected_text: str) -> None:
        loader = TextLoader()
        text = loader.load_text_with_id(TEST_ID)

        assert text.id == TEST_ID
        assert text.text == expected_text
        assert len(text.discourses) == NO_DISCOURSES


@pytest.fixture
def expected_text() -> str:
    with open(TRAIN_DIR + TEST_ID + ".txt", "r") as f:
        return f.read()

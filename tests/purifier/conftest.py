import pytest
from src.purifier import Purifier


@pytest.fixture
def purifier() -> Purifier:
    return Purifier()

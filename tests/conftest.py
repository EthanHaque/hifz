import pytest

from hifz.models import Card


@pytest.fixture
def flashcards():
    """Fixture to provide a list of sample flashcards."""
    return [
        Card("Capital of France?", "Paris"),
        Card("Capital of Germany?", "Berlin"),
        Card("Capital of Italy?", "Rome"),
    ]

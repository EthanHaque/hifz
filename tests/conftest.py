import pytest

from hifz.models import Card


@pytest.fixture
def cards():
    """Fixture to provide a list of sample cards."""
    return [
        Card("Capital of France?", "Paris"),
        Card("Capital of Germany?", "Berlin"),
        Card("Capital of Italy?", "Rome"),
    ]

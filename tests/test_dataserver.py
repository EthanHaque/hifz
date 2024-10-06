from hifz.dataserver import DataServer
from hifz.models import Card


def test_dataserver_returns_card():
    server = DataServer()
    cards = server.read_entries("data/arabic_letters.csv")
    assert Card("ب", "baa'") in cards

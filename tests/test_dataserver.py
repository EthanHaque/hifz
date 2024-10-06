from hifz.dataserver import DataServer


def test_dataserver():
    arabic_cards = DataServer("data/arabic_letters.csv")
    arabic_cards.get_cards()

from hifz import utils


def test_card_init():
    card = utils.Card("front", "back")
    assert card.front == "front"
    assert card.back == "back"

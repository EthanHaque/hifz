from hifz.card_engine import CardEngine
from hifz.learning_strategies import RandomStrategy, SequentialStrategy


def test_load_cards(utf8_test_file):
    engine = CardEngine(SequentialStrategy())
    assert engine.load_cards(str(utf8_test_file)) is True
    assert len(engine.session.cards) == 2


def test_get_next_card(utf8_test_file):
    engine = CardEngine(SequentialStrategy())
    engine.load_cards(str(utf8_test_file))
    card = engine.get_next_card()
    assert card.front == "ب"


def test_process_feedback(utf8_test_file):
    engine = CardEngine(SequentialStrategy())
    engine.load_cards(str(utf8_test_file))
    card = engine.get_next_card()

    engine.process_feedback(card, correct=True)
    assert card.performance.correct_guesses == 1


def test_reload_cards(utf8_test_file):
    engine = CardEngine(RandomStrategy())
    assert engine.load_cards(str(utf8_test_file)) is True
    assert engine.reload_cards(str(utf8_test_file)) is True
    assert len(engine.session.cards) == 2

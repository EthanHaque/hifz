from hifz.card_engine import CardEngine
from hifz.learning_strategies import SequentialStrategy, RandomStrategy


def test_load_cards(mock_dataserver):
    engine = CardEngine(SequentialStrategy())
    assert engine.load_cards("dummy_path") is True
    assert len(engine.session.cards) == 2


def test_get_next_card(mock_dataserver):
    engine = CardEngine(SequentialStrategy())
    engine.load_cards("dummy_path")
    card = engine.get_next_card()
    assert card.front == "Question 1"


def test_process_feedback(mock_dataserver):
    engine = CardEngine(SequentialStrategy())
    engine.load_cards("dummy_path")
    card = engine.get_next_card()

    engine.process_feedback(card, correct=True)
    assert card.performance.correct_guesses == 1


def test_reload_cards(mock_dataserver):
    engine = CardEngine(RandomStrategy())
    assert engine.load_cards("dummy_path") is True
    assert engine.reload_cards("dummy_path") is True
    assert len(engine.session.cards) == 2

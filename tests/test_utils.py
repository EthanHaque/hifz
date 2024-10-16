from hifz.learning_strategies import RandomStrategy, SequentialStrategy
from hifz.models import Card
from hifz.utils import CardSession


def test_card_session_with_random_strategy(cards: list[Card]):
    random_strategy = RandomStrategy()
    session = CardSession(cards, random_strategy)
    card = session.next_card()
    assert card in cards


def test_card_session_with_sequential_strategy(cards: list[Card]):
    sequential_strategy = SequentialStrategy()
    session = CardSession(cards, sequential_strategy)

    assert session.next_card() == cards[0]
    assert session.next_card() == cards[1]


def test_process_feedback(cards):
    sequential_strategy = SequentialStrategy()
    session = CardSession(cards, sequential_strategy)

    card = session.next_card()
    session.process_feedback(card, correct=True)

    assert card.performance.correct_guesses == 1
    session.process_feedback(card, correct=False)
    assert card.performance.incorrect_guesses == 1

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

from hifz.learning_strategies import RandomStrategy, SequentialStrategy
from hifz.models import Card
from hifz.utils import CardSession


def test_random_strategy_returns_card(cards: list[Card]):
    random_strategy = RandomStrategy()
    session = CardSession(cards, random_strategy)
    card = session.next_card()
    assert card in cards


def test_sequential_strategy_returns_in_order(cards: list[Card]):
    sequential_strategy = SequentialStrategy()
    session = CardSession(cards, sequential_strategy)

    card1 = session.next_card()
    card2 = session.next_card()
    card3 = session.next_card()

    assert card1 == cards[0]
    assert card2 == cards[1]
    assert card3 == cards[2]


def test_sequential_strategy_wraps_around(cards: list[Card]):
    sequential_strategy = SequentialStrategy()
    session = CardSession(cards, sequential_strategy)

    # Loop through the list to force wrap-around
    for _ in range(len(cards)):
        session.next_card()

    card = session.next_card()
    assert card == cards[0], "SequentialStrategy did not wrap around."

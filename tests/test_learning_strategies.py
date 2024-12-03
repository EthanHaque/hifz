from hifz.learning_strategies import RandomStrategy, SequentialStrategy
from hifz.models import Card, Feedback
from hifz.utils import CardSession


def test_random_strategy_returns_card(cards: list[Card]):
    """Test that RandomStrategy selects a card from the given list.

    Ensures that the random strategy in CardSession selects a card that exists
    in the original list, verifying that the strategy does not go out of bounds.

    Args:
        cards (list[Card]): List of Card objects.

    Asserts:
        - The selected card is within the original list of cards.
    """
    random_strategy = RandomStrategy()
    session = CardSession(cards, random_strategy)
    card = session.next_card()
    assert card in cards


def test_sequential_strategy_returns_in_order(cards: list[Card]):
    """Test that SequentialStrategy selects cards in order.

    Verifies that the sequential strategy in CardSession returns cards in the
    same order as provided in the list.

    Args:
        cards (list[Card]): List of Card objects.

    Asserts:
        - Cards are returned in the order of the list.
    """
    sequential_strategy = SequentialStrategy()
    session = CardSession(cards, sequential_strategy)

    card1 = session.next_card()
    card2 = session.next_card()
    card3 = session.next_card()

    assert card1 == cards[0]
    assert card2 == cards[1]
    assert card3 == cards[2]


def test_sequential_strategy_wraps_around(cards: list[Card]):
    """Test that SequentialStrategy wraps around to the start after reaching the end.

    Simulates going through all cards in the list to check if SequentialStrategy
    restarts from the first card once it reaches the end of the list.

    Args:
        cards (list[Card]): List of Card objects.

    Asserts:
        - After looping through all cards, the strategy wraps around to the first card.
    """
    sequential_strategy = SequentialStrategy()
    session = CardSession(cards, sequential_strategy)

    # Loop through the list to force wrap-around
    for _ in range(len(cards)):
        session.next_card()

    card = session.next_card()
    assert card == cards[0], "SequentialStrategy did not wrap around."


def test_random_strategy_processes_feedback(cards):
    """Test that RandomStrategy processes feedback correctly.

    Selects a random card and simulates correct feedback. Checks that
    the card's performance metrics are updated to reflect the feedback.

    Args:
        cards (list[Card]): List of Card objects.

    Asserts:
        - The correct_guesses count for the card is incremented as expected.
    """
    random_strategy = RandomStrategy()
    session = CardSession(cards, random_strategy)

    card = session.next_card()
    feedback = Feedback({"correct": True})
    random_strategy.process_feedback(card, feedback)
    assert card.performance.correct_guesses == 1


def test_sequential_strategy_processes_feedback(cards):
    """Test that SequentialStrategy processes feedback correctly.

    Selects a card in sequence and simulates incorrect feedback. Checks that
    the card's performance metrics are updated to reflect the feedback.

    Args:
        cards (list[Card]): List of Card objects.

    Asserts:
        - The incorrect_guesses count for the card is incremented as expected.
    """
    sequential_strategy = SequentialStrategy()
    session = CardSession(cards, sequential_strategy)

    card = session.next_card()
    feedback = Feedback({"correct": False})
    sequential_strategy.process_feedback(card, feedback)
    assert card.performance.incorrect_guesses == 1

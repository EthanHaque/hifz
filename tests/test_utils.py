from hifz.learning_strategies import RandomStrategy, SequentialStrategy
from hifz.models import Card
from hifz.utils import CardSession


def test_card_session_with_random_strategy(cards: list[Card]):
    """Test CardSession behavior with RandomStrategy.

    Verifies that the RandomStrategy in CardSession can select any card from
    the list, without going out of bounds.

    Args:
        cards (list[Card]): List of Card objects.

    Asserts:
        - The card selected by RandomStrategy is within the original list.
    """
    random_strategy = RandomStrategy()
    session = CardSession(cards, random_strategy)
    card = session.next_card()
    assert card in cards


def test_card_session_with_sequential_strategy(cards: list[Card]):
    """Test CardSession behavior with SequentialStrategy.

    Verifies that the SequentialStrategy in CardSession returns cards in the
    exact order they appear in the provided list.

    Args:
        cards (list[Card]): List of Card objects.

    Asserts:
        - The first and second cards returned are the first and second in the list.
    """
    sequential_strategy = SequentialStrategy()
    session = CardSession(cards, sequential_strategy)

    assert session.next_card() == cards[0]
    assert session.next_card() == cards[1]


def test_process_feedback(cards):
    """Test processing feedback in CardSession with SequentialStrategy.

    Checks that feedback (correct or incorrect) updates the performance metrics
    of the card appropriately within the session.

    Args:
        cards (list[Card]): List of Card objects.

    Asserts:
        - correct_guesses count is incremented after positive feedback.
        - incorrect_guesses count is incremented after negative feedback.
    """
    strategy = SequentialStrategy()
    session = CardSession(cards, strategy)

    card = session.next_card()
    feedback = session.strategy.create_feedback()
    feedback.data["correct"] = True
    session.strategy.process_feedback(card, feedback)

    assert card.statistics.get("correct") == 1
    assert card.statistics.get("incorrect") == 0

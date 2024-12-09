from datetime import datetime, timedelta

from hifz.learning_strategies import (
    AlphabeticalStrategy,
    MasteryStrategy,
    RandomStrategy,
    SequentialStrategy,
    SimpleSpacedRepetitionStrategy,
)
from hifz.models import Card
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


def test_mastery_strategy_prioritizes_low_correct_cards():
    """Test MasteryStrategy prioritizes cards with fewer correct responses."""
    mastery_strategy = MasteryStrategy(threshold=10)
    card1 = Card("Front1", "Back1")
    card2 = Card("Front2", "Back2")
    card3 = Card("Front3", "Back3")

    card1.statistics.update("correct", 30, lambda _, new: new)
    card2.statistics.update("correct", 1, lambda _, new: new)
    card3.statistics.update("correct", 50, lambda _, new: new)

    session = CardSession([card1, card2, card3], mastery_strategy)
    next_card = session.next_card()

    assert (
        next_card == card2
    ), "MasteryStrategy did not prioritize the card with fewer correct responses."


def test_mastery_strategy_processes_feedback_correctly():
    """Test MasteryStrategy updates card statistics correctly."""
    mastery_strategy = MasteryStrategy()
    card = Card("Front1", "Back1")

    feedback = mastery_strategy.create_feedback()
    feedback.data["correct"] = True
    mastery_strategy.process_feedback(card, feedback)

    assert (
        card.statistics.get("correct") == 1
    ), "MasteryStrategy did not correctly update the 'correct' statistic."


def test_spaced_repetition_schedules_next_review():
    """Test SimpleSpacedRepetitionStrategy schedules the next review correctly."""
    spaced_strategy = SimpleSpacedRepetitionStrategy()
    card = Card("Front1", "Back1")

    feedback = spaced_strategy.create_feedback()
    feedback.data["correct"] = True
    spaced_strategy.process_feedback(card, feedback)

    assert (
        "due" in card.statistics.data
    ), "SimpleSpacedRepetitionStrategy did not schedule the next review."
    assert (
        card.statistics.data["due"] > datetime.now()
    ), "Next review is not correctly scheduled."


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
    feedback = random_strategy.create_feedback()
    feedback.data["correct"] = True
    random_strategy.process_feedback(card, feedback)
    assert card.statistics.get("correct") == 1


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
    feedback = sequential_strategy.create_feedback()
    feedback.data["correct"] = True
    sequential_strategy.process_feedback(card, feedback)
    assert card.statistics.get("correct") == 1


def test_simple_spaced_repetition_strategy_process_feedback_interval_increase(
    monkeypatch, mocker, cards
):
    """Test that intervals increase with correct feedback."""
    mock_now = datetime(2023, 12, 1, 10, 0, 0)
    datetime_mock = mocker.MagicMock()
    datetime_mock.now.return_value = mock_now
    monkeypatch.setattr("hifz.learning_strategies.datetime", datetime_mock)

    spaced_repetition_strategy = SimpleSpacedRepetitionStrategy()
    session = CardSession(cards, spaced_repetition_strategy)

    card = session.next_card()

    feedback = spaced_repetition_strategy.create_feedback()
    feedback.data["correct"] = True
    spaced_repetition_strategy.process_feedback(card, feedback)
    prev_interval = card.statistics.get("interval")

    feedback = spaced_repetition_strategy.create_feedback()
    feedback.data["correct"] = True
    spaced_repetition_strategy.process_feedback(card, feedback)
    curr_interval = card.statistics.get("interval")

    assert curr_interval > prev_interval

    next_due = mock_now + timedelta(days=curr_interval)
    assert card.statistics.get("due") == next_due


def test_simple_spaced_repetition_strategy_process_feedback_interval_decrease(
    monkeypatch, mocker, cards
):
    """Test that intervals decrease with incorrect feedback."""
    mock_now = datetime(2023, 12, 1, 10, 0, 0)
    datetime_mock = mocker.MagicMock()
    datetime_mock.now.return_value = mock_now
    monkeypatch.setattr("hifz.learning_strategies.datetime", datetime_mock)

    spaced_repetition_strategy = SimpleSpacedRepetitionStrategy()
    session = CardSession(cards, spaced_repetition_strategy)

    card = session.next_card()

    feedback = spaced_repetition_strategy.create_feedback()
    feedback.data["correct"] = True
    spaced_repetition_strategy.process_feedback(card, feedback)
    prev_interval = card.statistics.get("interval")

    feedback = spaced_repetition_strategy.create_feedback()
    feedback.data["correct"] = False
    spaced_repetition_strategy.process_feedback(card, feedback)
    curr_interval = card.statistics.get("interval")

    assert curr_interval < prev_interval

    next_due = mock_now + timedelta(days=curr_interval)
    assert card.statistics.get("due") == next_due


def test_simple_spaced_repetition_strategy_process_feedback_compare_intervals(
    monkeypatch, mocker, cards
):
    """Test that cards answered correctly have longer intervals than cards answered incorrectly."""
    mock_now = datetime(2023, 12, 1, 10, 0, 0)
    datetime_mock = mocker.MagicMock()
    datetime_mock.now.return_value = mock_now
    monkeypatch.setattr("hifz.learning_strategies.datetime", datetime_mock)

    spaced_repetition_strategy = SimpleSpacedRepetitionStrategy()

    for card in cards[:-1]:
        feedback = spaced_repetition_strategy.create_feedback()
        feedback.data["correct"] = True
        spaced_repetition_strategy.process_feedback(card, feedback)

    card = cards[-1]
    feedback = spaced_repetition_strategy.create_feedback()
    feedback.data["correct"] = False
    spaced_repetition_strategy.process_feedback(card, feedback)

    for card in cards[:-1]:
        assert card.statistics.get("interval") > cards[-1].statistics.get("interval")


def test_spaced_repetition_prioritizes_due_cards():
    """Test SimpleSpacedRepetitionStrategy prioritizes cards that are due."""
    spaced_strategy = SimpleSpacedRepetitionStrategy()
    card1 = Card("Front1", "Back1")
    card2 = Card("Front2", "Back2")
    card3 = Card("Front3", "Back3")

    now = datetime.now()
    card1.statistics.update("due", now - timedelta(days=1), lambda _, new: new)
    card2.statistics.update("due", now + timedelta(days=1), lambda _, new: new)
    card3.statistics.update("due", now - timedelta(hours=2), lambda _, new: new)

    session = CardSession([card1, card2, card3], spaced_strategy)
    next_card = session.next_card()

    assert next_card in [
        card1,
        card3,
    ], "SimpleSpacedRepetitionStrategy did not prioritize due cards."


def test_spaced_repetition_selects_random_for_no_due_cards():
    """Test SimpleSpacedRepetitionStrategy selects randomly if no cards are due."""
    spaced_strategy = SimpleSpacedRepetitionStrategy()
    card1 = Card("Front1", "Back1")
    card2 = Card("Front2", "Back2")

    now = datetime.now()
    card1.statistics.update("due", now + timedelta(days=1), lambda _, new: new)
    card2.statistics.update("due", now + timedelta(days=2), lambda _, new: new)

    session = CardSession([card1, card2], spaced_strategy)
    next_card = session.next_card()

    assert next_card in [
        card1,
        card2,
    ], "SimpleSpacedRepetitionStrategy did not select randomly for non-due cards."


def test_mastery_strategy_serialization():
    """Test MasteryStrategy state serialization and deserialization."""
    mastery_strategy = MasteryStrategy(threshold=10)
    mastery_strategy.index = 3

    serialized = mastery_strategy.to_dict()
    assert serialized == {
        "type": "MasteryStrategy",
        "state": {
            "index": 3,
            "threshold": 10,
        },
    }, "MasteryStrategy did not serialize correctly."

    deserialized = MasteryStrategy.from_dict(serialized)
    assert isinstance(
        deserialized, MasteryStrategy
    ), "Deserialized object is not of type MasteryStrategy."
    assert (
        deserialized.threshold == 10
    ), "Deserialized MasteryStrategy has incorrect 'threshold'."
    assert (
        deserialized.index == 3
    ), "Deserialized MasteryStrategy has incorrect 'index'."


def test_spaced_repetition_strategy_serialization():
    """Test SimpleSpacedRepetitionStrategy state serialization and deserialization."""
    spaced_strategy = SimpleSpacedRepetitionStrategy()

    serialized = spaced_strategy.to_dict()
    deserialized = SimpleSpacedRepetitionStrategy.from_dict(serialized)

    assert isinstance(
        deserialized, SimpleSpacedRepetitionStrategy
    ), "Failed to deserialize strategy correctly."


def test_alphabetal_strategy_ordering():
    """Tests that the AlphabeticalStrategy sorts cards correctly."""

    alpha_strategy = AlphabeticalStrategy()
    card1 = Card("B", "Second")
    card2 = Card("A", "First")
    card3 = Card("C", "Third")

    session = CardSession([card1, card2, card3], alpha_strategy)
    assert session.next_card() == card2
    assert session.next_card() == card1
    assert session.next_card() == card3

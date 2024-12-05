import json

import pytest

from hifz.learning_strategies import MasteryStrategy, RandomStrategy, SequentialStrategy
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


def test_card_session_save_and_load_with_random_strategy(tmp_path_factory):
    """Test saving and loading a session with RandomStrategy."""
    tmp_dir = tmp_path_factory.mktemp("session_data")
    save_file = tmp_dir / "session.json"

    cards = [Card("Front1", "Back1"), Card("Front2", "Back2")]
    strategy = RandomStrategy()
    session = CardSession(cards, strategy)

    session.save_progress(save_file)

    loaded_session = CardSession.load_progress(save_file)

    assert isinstance(loaded_session.strategy, RandomStrategy)
    assert len(loaded_session.cards) == len(cards)
    for original, loaded in zip(cards, loaded_session.cards, strict=True):
        assert original.front == loaded.front
        assert original.back == loaded.back


def test_card_session_save_and_load_with_sequential_strategy(tmp_path_factory):
    """Test saving and loading a session with SequentialStrategy."""
    tmp_dir = tmp_path_factory.mktemp("session_data")
    save_file = tmp_dir / "session.json"

    cards = [Card("Front1", "Back1"), Card("Front2", "Back2")]
    strategy = SequentialStrategy()
    session = CardSession(cards, strategy)

    session.save_progress(save_file)

    loaded_session = CardSession.load_progress(save_file)

    assert isinstance(loaded_session.strategy, SequentialStrategy)
    assert len(loaded_session.cards) == len(cards)
    for original, loaded in zip(cards, loaded_session.cards, strict=True):
        assert original.front == loaded.front
        assert original.back == loaded.back


def test_card_session_save_and_load_with_mastery_strategy(tmp_path_factory):
    """Test saving and loading a session with MasteryStrategy."""
    tmp_dir = tmp_path_factory.mktemp("session_data")
    save_file = tmp_dir / "session.json"

    cards = [Card("Front1", "Back1"), Card("Front2", "Back2")]
    strategy = MasteryStrategy(threshold=10)
    session = CardSession(cards, strategy)

    session.save_progress(save_file)

    loaded_session = CardSession.load_progress(save_file)

    assert isinstance(loaded_session.strategy, MasteryStrategy)
    assert loaded_session.strategy.threshold == 10
    assert len(loaded_session.cards) == len(cards)
    for original, loaded in zip(cards, loaded_session.cards, strict=True):
        assert original.front == loaded.front
        assert original.back == loaded.back


def test_card_session_load_with_unsupported_strategy(tmp_path_factory):
    """Test loading a session with an unsupported strategy."""
    tmp_dir = tmp_path_factory.mktemp("session_data")
    save_file = tmp_dir / "session.json"

    invalid_data = {
        "metadata": {"version": "1.0", "timestamp": "2023-12-01T12:34:56Z"},
        "session": {
            "strategy": {"type": "NonExistentStrategy", "state": {}},
            "cards": [{"front": "Front1", "back": "Back1"}],
        },
    }
    save_file.write_text(json.dumps(invalid_data, indent=4))

    with pytest.raises(
        ValueError, match="Unsupported strategy type: NonExistentStrategy"
    ):
        CardSession.load_progress(save_file)

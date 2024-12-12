import pytest

from hifz.card_engine import CardEngine
from hifz.learning_strategies import (
    MasteryStrategy,
    RandomStrategy,
    SequentialStrategy,
    SimpleSpacedRepetitionStrategy,
)


def test_load_cards(utf8_test_file):
    """Test the load_cards method of CardEngine with a UTF-8 encoded file.

    Verifies that cards are successfully loaded from the specified file,
    and that the loaded card count matches the expected number.

    Args:
        utf8_test_file (Path): Path to a CSV file with UTF-8 encoded content.

    Asserts:
        - load_cards() returns True if cards were successfully loaded
        - The number of cards currently loaded is 2
    """
    engine = CardEngine(SequentialStrategy())
    assert engine.load_cards(str(utf8_test_file)) is True
    assert len(engine.session.cards) == 2


def test_get_next_card(utf8_test_file):
    """Test retrieving the next card in the sequence.

    Ensures that, after loading cards, the first card returned by get_next_card()
    matches the expected content, verifying that the sequence works as expected.

    Args:
        utf8_test_file (Path): Path to a CSV file with UTF-8 encoded content.

    Asserts:
        - The 'front' field of the first card matches the expected Arabic character, ب.
    """
    engine = CardEngine(SequentialStrategy())
    engine.load_cards(str(utf8_test_file))
    card = engine.get_next_card()
    assert card.front == "ب"


def test_process_feedback(utf8_test_file):
    """Test processing feedback for a card's performance.

    Simulates giving correct feedback for a card and verifies that the performance
    metrics (correct guesses) are updated accordingly.

    Args:
        utf8_test_file (Path): Path to a CSV file with UTF-8 encoded content.

    Asserts:
        - The correct_guesses count for the card is incremented to 1.
    """
    engine = CardEngine(SequentialStrategy())
    engine.load_cards(str(utf8_test_file))
    card = engine.get_next_card()

    feedback = engine.get_feedback()
    feedback.data["correct"] = True
    engine.process_feedback(card, feedback)

    assert card.statistics.get("correct") == 1


def test_reload_cards(utf8_test_file):
    """Test reloading cards into the CardEngine.

    Loads cards from a file, then reloads them to ensure that the reload function
    works correctly and maintains the correct number of cards.

    Args:
        utf8_test_file (Path): Path to a CSV file with UTF-8 encoded content.

    Asserts:
        - load_cards() returns True if cards were successfully loaded
        - reload_cards() returns True if cards were successfully reloaded
        - The card count remains consistent (2) after reloading.
    """
    engine = CardEngine(RandomStrategy())
    assert engine.load_cards(str(utf8_test_file)) is True
    assert engine.reload_cards(str(utf8_test_file)) is True
    assert len(engine.session.cards) == 2


def test_engine_unsupported_file_extension(tmp_path_factory):
    """Test loading a file with an unsupported file extension.

    Attempts to load a file with an unsupported extension and checks that
    load_cards() returns False, indicating failure to load the file.

    Args:
        tmp_path_factory (TempPathFactory): Factory for creating temporary files.

    Asserts:
        - load_cards() returns False when attempting to load an unsupported file type.
    """
    engine = CardEngine(RandomStrategy())
    unsupported_file = tmp_path_factory.mktemp("data") / "unsupported.unsupported"
    unsupported_file.write_text("This is an unsupported file.")
    assert engine.load_cards(str(unsupported_file)) is False


def test_engine_save_progress(tmp_path_factory, utf8_test_file):
    """Test saving the current session state to a file."""
    tmp_dir = tmp_path_factory.mktemp("session_data")
    save_file = tmp_dir / "session.json"

    engine = CardEngine(SequentialStrategy())
    engine.load_cards(utf8_test_file)
    engine.save_progress(save_file)

    assert save_file.exists(), "Progress file was not created."
    assert save_file.read_text(), "Progress file is empty."


def test_engine_load_progress(tmp_path_factory, utf8_test_file):
    """Test loading a session state from a saved progress file."""
    tmp_dir = tmp_path_factory.mktemp("session_data")
    save_file = tmp_dir / "session.json"

    engine = CardEngine(SequentialStrategy())
    engine.load_cards(utf8_test_file)
    engine.save_progress(save_file)

    new_engine = CardEngine(SequentialStrategy())
    new_engine.load_progress(save_file)

    assert len(new_engine.session.cards) == len(engine.session.cards)
    for original, loaded in zip(
        engine.session.cards, new_engine.session.cards, strict=True
    ):
        assert original.front == loaded.front
        assert original.back == loaded.back


def test_engine_save_and_load_with_random_strategy(tmp_path_factory, utf8_test_file):
    """Test saving and loading session state with RandomStrategy."""
    tmp_dir = tmp_path_factory.mktemp("session_data")
    save_file = tmp_dir / "session.json"

    engine = CardEngine(RandomStrategy())
    engine.load_cards(utf8_test_file)
    engine.save_progress(save_file)

    new_engine = CardEngine(RandomStrategy())
    new_engine.load_progress(save_file)

    assert isinstance(new_engine.strategy, RandomStrategy)
    assert len(new_engine.session.cards) == len(engine.session.cards)


def test_engine_save_and_load_with_mastery_strategy(tmp_path_factory, utf8_test_file):
    """Test saving and loading session state with MasteryStrategy."""
    tmp_dir = tmp_path_factory.mktemp("session_data")
    save_file = tmp_dir / "session.json"

    engine = CardEngine(MasteryStrategy(threshold=10))
    engine.load_cards(utf8_test_file)
    engine.save_progress(save_file)

    new_engine = CardEngine(MasteryStrategy())
    new_engine.load_progress(save_file)

    assert isinstance(new_engine.strategy, MasteryStrategy)
    assert new_engine.strategy.threshold == 10
    assert len(new_engine.session.cards) == len(engine.session.cards)


def test_engine_load_with_invalid_strategy(tmp_path_factory, utf8_test_file):
    """Test loading a session with an unsupported strategy type."""
    tmp_dir = tmp_path_factory.mktemp("session_data")
    save_file = tmp_dir / "session.json"

    engine = CardEngine(SequentialStrategy())
    engine.load_cards(utf8_test_file)
    engine.save_progress(save_file)

    save_data = save_file.read_text()
    save_data = save_data.replace("SequentialStrategy", "NonExistentStrategy")
    save_file.write_text(save_data)

    new_engine = CardEngine(SequentialStrategy())
    with pytest.raises(
        ValueError, match="Unsupported strategy type: NonExistentStrategy"
    ):
        new_engine.load_progress(save_file)


def test_global_statistics(utf8_test_file):
    """Test global session statistics."""
    engine = CardEngine(RandomStrategy())
    engine.load_cards(str(utf8_test_file))
    for _ in range(5):
        card = engine.get_next_card()
        feedback = engine.get_feedback()
        feedback.data["correct"] = True
        engine.process_feedback(card, feedback)
    for _ in range(3):
        card = engine.get_next_card()
        feedback = engine.get_feedback()
        feedback.data["correct"] = False
        engine.process_feedback(card, feedback)
    assert engine.session.aggregate_statistics() == {"Correct": 5, "Incorrect": 3}


def test_spaced_repetition_serialization(utf8_test_file, tmp_path_factory):
    """Tests card seralization for the SSR strategy."""
    engine = CardEngine(SimpleSpacedRepetitionStrategy())
    engine.load_cards(utf8_test_file)
    for _ in range(5):
        card = engine.get_next_card()
        feedback = engine.get_feedback()
        feedback.data["correct"] = True
        engine.process_feedback(card, feedback)

    output_path = tmp_path_factory.mktemp("saves") / "save.json"
    engine.save_progress(output_path)
    engine.load_progress(output_path)

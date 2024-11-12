from hifz.card_engine import CardEngine
from hifz.learning_strategies import RandomStrategy, SequentialStrategy


def test_load_cards(utf8_test_file):
    """
    Test the load_cards method of CardEngine with a UTF-8 encoded file.
    
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
    """
    Test retrieving the next card in the sequence.
    
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
    """
    Test processing feedback for a card's performance.
    
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

    engine.process_feedback(card, correct=True)
    assert card.performance.correct_guesses == 1


def test_reload_cards(utf8_test_file):
    """
    Test reloading cards into the CardEngine.

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
    """
    Test loading a file with an unsupported file extension.

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

import pytest

from hifz.models import Card


@pytest.fixture
def csv_file(tmp_path_factory):
    """
    Fixture that creates a temporary CSV file for testing.
    
    The CSV file contains sample Arabic characters and their English transliterations.
    It includes two columns: 'front' and 'back', representing the question and answer sides
    of a card, respectively.
    
    Returns:
        Path to the temporary CSV file.
    """
    tmp_file_path = tmp_path_factory.mktemp("data") / "test_arabic.csv"
    with tmp_file_path.open("w", encoding="utf-8") as f:
        f.writelines(["front,back\n", "ب,baa\n"])
    return tmp_file_path


@pytest.fixture
def json_file(tmp_path_factory):
    """
    Fixture that creates a temporary JSON file for testing.
    
    The JSON file contains Arabic characters with their English transliterations,
    stored as dictionaries with 'front' and 'back' keys representing question and answer.
    
    Returns:
        Path to the temporary JSON file.
    """
    tmp_file_path = tmp_path_factory.mktemp("data") / "test_arabic.json"
    with tmp_file_path.open("w", encoding="utf-8") as f:
        f.write('[{"front": "ب", "back": "baa"}]')
    return tmp_file_path


@pytest.fixture
def utf8_test_file(tmp_path_factory):
    """
    Fixture that creates a temporary CSV file with UTF-8 encoded content for testing.
    
    The CSV file contains sample characters in multiple languages (Arabic and Kanji),
    allowing testing of UTF-8 encoding support. Columns are labeled 'front' and 'back'.
    
    Returns:
        Path to the temporary CSV file with UTF-8 encoded content.
    """
    tmp_file_path = tmp_path_factory.mktemp("data") / "utf8_test.csv"
    utf8_content = "front,back\nب,baa\n漢字,kanji\n"
    with tmp_file_path.open("w", encoding="utf-8") as f:
        f.write(utf8_content)
    return tmp_file_path


@pytest.fixture
def cards():
    """
    Fixture that provides a sample list of Card objects.
    
    This list simulates a set of flashcards with questions about European capitals
    and their respective answers.
    
    Returns:
        List of Card objects with sample data.
    """
    return [
        Card("Capital of France?", "Paris"),
        Card("Capital of Germany?", "Berlin"),
        Card("Capital of Italy?", "Rome"),
    ]

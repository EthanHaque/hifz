import xml.dom.minidom as xml

import pytest

from hifz.models import Card


@pytest.fixture
def csv_file(tmp_path_factory):
    """Fixture that creates a temporary CSV file for testing.

    The CSV file contains sample Arabic characters and their English transliterations.
    It includes two columns: 'front' and 'back', representing the question and answer sides
    of a card, respectively.

    Args:
        tmp_path_factory (TempPathFactory): Fixture for creating temporary paths.

    Returns:
        tmp_file_path (TempPathFactory): Path to the temporary CSV file.
    """
    tmp_file_path = tmp_path_factory.mktemp("data") / "test_arabic.csv"
    with tmp_file_path.open("w", encoding="utf-8") as f:
        f.writelines(["front,back\n", "ب,baa\n"])
    return tmp_file_path


@pytest.fixture
def tsv_file(tmp_path_factory):
    """Fixture that creates a temporary tsv file for testing.

    The tsv file contains sample Arabic characters and their English transliterations.
    It includes two columns: 'front' and 'back', representing the question and answer sides
    of a card, respectively.

    Args:
        tmp_path_factory (TempPathFactory): Fixture for creating temporary paths.

    Returns:
        tmp_file_path (TempPathFactory): Path to the temporary tsv file.
    """
    tmp_file_path = tmp_path_factory.mktemp("data") / "test_arabic.tsv"
    with tmp_file_path.open("w", encoding="utf-8") as f:
        f.writelines(["front\tback\n", "ب\tbaa\n"])
    return tmp_file_path


@pytest.fixture
def json_file(tmp_path_factory):
    """Fixture that creates a temporary JSON file for testing.

    The JSON file contains Arabic characters with their English transliterations,
    stored as dictionaries with 'front' and 'back' keys representing question and answer
    sides of a card, respectively.

    Args:
        tmp_path_factory (TempPathFactory): Fixture for creating temporary paths.

    Returns:
        tmp_file_path (TempPathFactory): Path to the temporary JSON file.
    """
    tmp_file_path = tmp_path_factory.mktemp("data") / "test_arabic.json"
    with tmp_file_path.open("w", encoding="utf-8") as f:
        f.write('[{"front": "ب", "back": "baa"}]')
    return tmp_file_path


@pytest.fixture
def xml_file(tmp_path_factory):
    """Fixture that creates a temporary XML file for testing.

    The XML file contains Arabic characters with their English transliterations,
    stored as dictionaries with 'front' and 'back' keys representing question and answer
    sides of a card, respectively.

    Args:
        tmp_path_factory (TempPathFactory): Fixture for creating temporary paths.

    Returns:
        tmp_file_path (TempPathFactory): Path to the temporary XML file.
    """
    tmp_file_path = tmp_path_factory.mktemp("data") / "test_arabic.xml"
    doc = xml.Document()

    root = doc.createElement("cards")
    doc.appendChild(root)

    card_element = doc.createElement("card")
    root.appendChild(card_element)

    front_element = doc.createElement("front")
    front_text = doc.createTextNode("ب")
    front_element.appendChild(front_text)
    card_element.appendChild(front_element)

    back_element = doc.createElement("back")
    back_text = doc.createTextNode("baa")
    back_element.appendChild(back_text)
    card_element.appendChild(back_element)

    xml_str = doc.toprettyxml(indent="  ", encoding="utf-8")
    with tmp_file_path.open("wb") as f:
        f.write(xml_str)

    return tmp_file_path


@pytest.fixture
def utf8_test_file(tmp_path_factory):
    """Fixture that creates a temporary CSV file with UTF-8 encoded content for testing.

    The CSV file contains sample characters in multiple languages (Arabic and Kanji),
    allowing testing of UTF-8 encoding support. Columns are labeled 'front' and 'back'.

    Args:
        tmp_path_factory (TempPathFactory): Fixture for creating temporary paths.

    Returns:
        tmp_file_path (TempPathFactory): Path to the temporary CSV file with UTF-8 encoded content.
    """
    tmp_file_path = tmp_path_factory.mktemp("data") / "utf8_test.csv"
    utf8_content = "front,back\nب,baa\n漢字,kanji\n"
    with tmp_file_path.open("w", encoding="utf-8") as f:
        f.write(utf8_content)
    return tmp_file_path


@pytest.fixture
def cards():
    """Fixture that provides a sample list of Card objects.

    This list instanciates a test set of flashcards with questions about
    European countries and their respective capital cities.

    Returns:
        list(Card): List of Card objects with sample data.
    """
    return [
        Card("Capital of France?", "Paris"),
        Card("Capital of Germany?", "Berlin"),
        Card("Capital of Italy?", "Rome"),
    ]

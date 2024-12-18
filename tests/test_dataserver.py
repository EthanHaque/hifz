import pytest

from hifz.dataserver import DataServer
from hifz.models import Card


def test_utf8_encoding_support(utf8_test_file):
    """Test that DataServer can correctly read entries from a UTF-8 encoded file.

    Verifies that cards with multi-language content (Arabic and Kanji) are
    properly recognized and stored as Card objects.

    Args:
        utf8_test_file (Path): Path to a CSV file with UTF-8 encoded content.

    Asserts:
        - Card("ب", "baa") is in the output list.
        - Card("漢字", "kanji") is in the output list.
    """
    server = DataServer()
    cards = server.read_cards(str(utf8_test_file))

    assert Card("ب", "baa") in cards
    assert Card("漢字", "kanji") in cards


def test_dataserver_returns_card_csv(csv_file):
    """Test that DataServer reads card entries from a CSV file correctly.

    Verifies that a simple CSV file is read and its contents are stored as Card objects.

    Args:
        csv_file (Path): Path to a CSV file with sample Arabic content.

    Asserts:
        - Card("ب", "baa") is in the output list.
    """
    server = DataServer()
    cards = server.read_cards(str(csv_file))
    assert Card("ب", "baa") in cards


def test_dataserver_returns_card_json(json_file):
    """Test that DataServer reads card entries from a JSON file correctly.

    Verifies that a JSON file with Arabic characters is read properly, and its contents
    are stored as Card objects.

    Args:
        json_file (Path): Path to a JSON file with sample Arabic content.

    Asserts:
        - Card("ب", "baa") is in the output list.
    """
    server = DataServer()
    cards = server.read_cards(str(json_file))
    assert Card("ب", "baa") in cards


def test_dataserver_returns_card_xml(xml_file):
    """Test that DataServer reads card entries from a XML file correctly.

    Verifies that a XML file with Arabic characters is read properly, and its contents
    are stored as Card objects.

    Args:
        xml_file (Path): Path to a XML file with sample Arabic content.

    Asserts:
        - Card("ب", "baa") is in the output list.
    """
    server = DataServer()
    cards = server.read_cards(str(xml_file))
    assert Card("ب", "baa") in cards


def test_dataserver_returns_card_tsv(tsv_file):
    """Test that DataServer reads card entries from a tsv file correctly.

    Verifies that a tsv file with Arabic characters is read properly, and its contents
    are stored as Card objects.

    Args:
        tsv_file (Path): Path to a tsv file with sample Arabic content.

    Asserts:
        - Card("ب", "baa") is in the output list.
    """
    server = DataServer()
    cards = server.read_cards(str(tsv_file))
    assert Card("ب", "baa") in cards


def test_dataserver_file_not_found():
    """Test that DataServer raises a FileNotFoundError for a non-existent file.

    Attempts to read from a file path that doesn't exist and verifies that
    the appropriate exception is raised with a clear error message.

    Asserts:
        - FileNotFoundError is raised with the correct error message.
    """
    server = DataServer()
    non_existent_file = "non_existent_file.csv"

    with pytest.raises(FileNotFoundError) as excinfo:
        server.read_cards(non_existent_file)

    assert f"Error: The file at path '{non_existent_file}' was not found." in str(
        excinfo.value
    )


def test_dataserver_empty_csv(tmp_path_factory):
    """Test that DataServer correctly handles an empty CSV file.

    Creates an empty CSV file (header only) and verifies that no cards are returned.

    Args:
        tmp_path_factory (TempPathFactory): Factory for creating temporary files.

    Asserts:
        - The output list is empty when reading from an empty CSV file.
    """
    server = DataServer()
    empty_csv_file = tmp_path_factory.mktemp("data") / "empty.csv"

    empty_csv_file.write_text("front,back\n")

    cards = server.read_cards(str(empty_csv_file))

    assert len(cards) == 0


def test_dataserver_empty_json(tmp_path_factory):
    """Test that DataServer correctly handles an empty JSON file.

    Creates an empty JSON array and verifies that no cards are returned.

    Args:
        tmp_path_factory (TempPathFactory): Factory for creating temporary files.

    Asserts:
        - The output list is empty when reading from an empty JSON file.
    """
    server = DataServer()
    empty_json_file = tmp_path_factory.mktemp("data") / "empty.json"

    empty_json_file.write_text("[]")

    cards = server.read_cards(str(empty_json_file))

    assert len(cards) == 0


def test_dataserver_unsupported_file_extension(tmp_path_factory):
    """Test that DataServer raises a ValueError for unsupported file extensions.

    Creates a file with an unsupported extension and verifies that the
    appropriate exception is raised with a clear error message.

    Args:
        tmp_path_factory (TempPathFactory): Factory for creating temporary files.

    Asserts:
        - ValueError is raised with the correct message for unsupported extensions.
    """
    server = DataServer()
    unsupported_file = tmp_path_factory.mktemp("data") / "unsupported.unsupported"
    unsupported_file.write_text("This is an unsupported file.")

    with pytest.raises(ValueError, match="Unsupported file extension: .unsupported"):
        server.read_cards(str(unsupported_file))


def test_dataserver_card_reversal(utf8_test_file):
    """Tests that card reversal works as expected."""
    server = DataServer()
    cards = server.read_cards(str(utf8_test_file), reverse=True)

    assert Card("baa", "ب") in cards
    assert Card("kanji", "漢字") in cards


def test_dataserver_reads_from_url(monkeypatch, mocker):
    """Test that DataServer correctly reads data from a URL."""
    mock_response = mocker.MagicMock()
    mock_response.read.return_value = b"front,back\nHello,World\nTest,Card\n"

    def mock_urlopen(url):
        _ = url
        return mock_response

    monkeypatch.setattr("hifz.dataserver.urlopen", mock_urlopen)

    server = DataServer()

    test_url = "http://example.com/test.csv"
    cards = server.read_cards(test_url)

    assert Card("Hello", "World") in cards
    assert Card("Test", "Card") in cards

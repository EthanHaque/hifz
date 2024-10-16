import pytest

from hifz.dataserver import DataServer
from hifz.models import Card


def test_utf8_encoding_support(utf8_test_file):
    server = DataServer()
    cards = server.read_entries(str(utf8_test_file))

    assert Card("ب", "baa") in cards
    assert Card("漢字", "kanji") in cards


def test_dataserver_returns_card_csv(csv_file):
    server = DataServer()
    cards = server.read_entries(str(csv_file))
    assert Card("ب", "baa") in cards


def test_dataserver_returns_card_json(json_file):
    server = DataServer()
    cards = server.read_entries(str(json_file))
    assert Card("ب", "baa") in cards


def test_dataserver_file_not_found():
    server = DataServer()
    non_existent_file = "non_existent_file.csv"

    with pytest.raises(FileNotFoundError) as excinfo:
        server.read_entries(non_existent_file)

    assert f"Error: The file at path '{non_existent_file}' was not found." in str(
        excinfo.value
    )


def test_dataserver_empty_csv(tmp_path_factory):
    server = DataServer()
    empty_csv_file = tmp_path_factory.mktemp("data") / "empty.csv"

    empty_csv_file.write_text("front,back\n")

    cards = server.read_entries(str(empty_csv_file))

    assert len(cards) == 0


def test_dataserver_empty_json(tmp_path_factory):
    server = DataServer()
    empty_json_file = tmp_path_factory.mktemp("data") / "empty.json"

    empty_json_file.write_text("[]")

    cards = server.read_entries(str(empty_json_file))

    assert len(cards) == 0


def test_dataserver_unsupported_file_extension(tmp_path_factory):
    server = DataServer()
    unsupported_file = tmp_path_factory.mktemp("data") / "unsupported.unsupported"
    unsupported_file.write_text("This is an unsupported file.")

    with pytest.raises(ValueError, match="Unsupported file extension: .unsupported"):
        server.read_entries(str(unsupported_file))

import pytest

from hifz.dataserver import DataServer
from hifz.models import Card


@pytest.fixture
def csv_file(tmp_path_factory):
    tmp_file_path = tmp_path_factory.mktemp("data") / "test_arabic.csv"
    with tmp_file_path.open("w", encoding="utf-8") as f:
        f.writelines(["front,back\n", "ب,baa\n"])
    return tmp_file_path


@pytest.fixture
def json_file(tmp_path_factory):
    tmp_file_path = tmp_path_factory.mktemp("data") / "test_arabic.json"
    with tmp_file_path.open("w", encoding="utf-8") as f:
        f.write('[{"front": "ب", "back": "baa"}]')
    return tmp_file_path


@pytest.fixture
def utf8_test_file(tmp_path_factory):
    tmp_file_path = tmp_path_factory.mktemp("data") / "utf8_test.csv"
    utf8_content = "front,back\nب,baa\n漢字,kanji\n"
    with tmp_file_path.open("w", encoding="utf-8") as f:
        f.write(utf8_content)
    return tmp_file_path


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

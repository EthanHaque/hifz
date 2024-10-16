from unittest.mock import patch

import pytest

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

@pytest.fixture
def cards():
    """Fixture to provide a list of sample cards."""
    return [
        Card("Capital of France?", "Paris"),
        Card("Capital of Germany?", "Berlin"),
        Card("Capital of Italy?", "Rome"),
    ]

@pytest.fixture
def mock_dataserver():
    with patch("hifz.card_engine.DataServer") as MockDataServer:
        mock_server = MockDataServer.return_value
        mock_server.read_entries.return_value = [
            Card("Question 1", "Answer 1"),
            Card("Question 2", "Answer 2"),
        ]
        yield mock_server
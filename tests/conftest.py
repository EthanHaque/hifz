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

from pathlib import Path

import pytest

from hifz.dataserver import DataServer
from hifz.models import Card


@pytest.fixture(scope="session")
def test_dataserver_returns_card_csv(tmp_path_factory):
    server = DataServer()
    tmp_file_path = tmp_path_factory.mktemp("test_arabic.csv")
    with Path(tmp_file_path).open(encoding="uft-8") as f:
        f.writelines(["front,back", "ب,baa"])
    cards = server.read_entries(tmp_file_path)
    assert Card("ب", "baa'") in cards


@pytest.fixture(scope="session")
def test_dataserver_returns_card_json(tmp_path_factory):
    server = DataServer()
    tmp_file_path = tmp_path_factory.mktemp("test_arabic.json")
    with Path(tmp_file_path).open(encoding="uft-8") as f:
        f.write(str([{"front": "ب", "back": "baa"}]))
    cards = server.read_entries(tmp_file_path)
    assert Card("ب", "baa'") in cards

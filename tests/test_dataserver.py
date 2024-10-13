from pathlib import Path

from hifz.dataserver import DataServer
from hifz.models import Card


def test_dataserver_returns_card_csv(tmp_file):
    server = DataServer()
    tmp_file_path = tmp_file / "test_arabic.csv"
    with Path(temp_file_path).open(encoding="uft-8") as f:
        f.writelines(["front,back", "ا,alif (a as in bad or A as in fAther)", "ب,baa"])
    cards = server.read_entries(temp_file_path)
    assert Card("ب", "baa'") in cards


def test_dataserver_returns_card_json(tmp_file):
    server = DataServer()
    tmp_file_path = tmp_file / "test_arabic.json"
    with Path(tmp_file_path).open(encoding="uft-8") as f:
        f.write(
            str(
                [
                    {"front": "ا", "back": "alif (a as in bad or A as in fAther)"},
                    {"front": "ب", "back": "baa"},
                ]
            )
        )
    cards = server.read_entries(temp_file_path)
    Path(temp_file_path).unlink()
    assert Card("ب", "baa'") in cards

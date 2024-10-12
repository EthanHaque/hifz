from pathlib import Path
from hifz.dataserver import DataServer
from hifz.models import Card

def test_dataserver_returns_card_csv():
    server = DataServer()
    temp_file_path = "data/test_arabic.csv"
    with Path(temp_file_path).open() as f:
        f.writelines([
            "front,back",
            "ا,alif (a as in bad or A as in fAther)",
            "ب,'baa"
            ])
    cards = server.read_entries(temp_file_path)
    Path(temp_file_path).unlink()
    assert Card("ب", "baa'") in cards

def test_dataserver_returns_card_json():
    server = DataServer()
    temp_file_path = "data/test_arabic.json"
    with Path(temp_file_path).open() as f:
        f.write(str([
        {
        "front": "ا",
        "back": "alif (a as in bad or A as in fAther)"
        },{
            "front": "ب",
            "back": "baa"
        }]))
    cards = server.read_entries(temp_file_path)
    Path(temp_file_path).unlink()
    assert Card("ب", "baa'") in cards

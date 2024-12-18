"""The dataserver module is responsible for serving content."""

import csv
import json
import tempfile
import xml.dom.minidom as xml
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

from hifz.models import Card


class FileInputStrategy(ABC):
    """This ABC is an interface for the delivery independent of file types."""

    @abstractmethod
    def read_cards(self, file_path: Path, reverse: bool = False) -> list[Card]:
        """Reads the entries from file_path."""


class CSVFileInputStrategy(FileInputStrategy):
    """This class maintains the logic for reading from csv files types."""

    def read_cards(self, file_path: Path, reverse: bool = False) -> list[Card]:
        """Reads the entries from the csv at file_path."""
        with file_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reverse:
                return [Card(e["back"], e["front"]) for e in reader]
            return [Card(e["front"], e["back"]) for e in reader]


class TSVFileInputStrategy(FileInputStrategy):
    """This class maintains the logic for reading from tsv files types."""

    def read_cards(self, file_path: Path, reverse: bool = False) -> list[Card]:
        """Reads the entries from the tsv at file_path."""
        with file_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            if reverse:
                return [Card(e["back"], e["front"]) for e in reader]
            return [Card(e["front"], e["back"]) for e in reader]


class JSONFileInputStrategy(FileInputStrategy):
    """This class maintains the logic for reading from json files types."""

    def read_cards(self, file_path: Path, reverse: bool = False) -> list[Card]:
        """Reads the entries from the json at file_path."""
        with file_path.open("r", encoding="utf-8") as f:
            entries = json.load(f)
            if reverse:
                return [Card(e["back"], e["front"]) for e in entries]
            return [Card(e["front"], e["back"]) for e in entries]


class XMLFileInputStrategy(FileInputStrategy):
    """This class maintains the logic for reading from XML files types."""

    def read_cards(self, file_path: Path, reverse: bool = False) -> list[Card]:
        """Reads the entries from the XML at file_path."""
        with file_path.open("r", encoding="utf-8") as f:
            dom = xml.parse(f)

        cards = []
        for card in dom.getElementsByTagName("card"):
            front_element = card.getElementsByTagName("front")[0].firstChild
            if not front_element:
                msg = f"Missing card front in {file_path}"
                raise ValueError(msg)
            if not isinstance(front_element, xml.Text):
                msg = "Front node is not of type Text"
                raise ValueError(msg)

            back_element = card.getElementsByTagName("back")[0].firstChild
            if not back_element:
                msg = f"Missing card back in {file_path}"
                raise ValueError(msg)
            if not isinstance(back_element, xml.Text):
                msg = "Back node is not of type Text"
                raise ValueError(msg)

            front_text = front_element.nodeValue
            back_text = back_element.nodeValue

            if reverse:
                cards.append(Card(back_text, front_text))
            else:
                cards.append(Card(front_text, back_text))
        return cards


class FileInputReader:
    """Dispatches the appropriate reader strategy based on file extension."""

    def __init__(self) -> None:
        """Instantiates the FileInputReader."""
        self.strategies = {
            ".csv": CSVFileInputStrategy(),
            ".json": JSONFileInputStrategy(),
            ".xml": XMLFileInputStrategy(),
            ".tsv": TSVFileInputStrategy(),
        }

    def get_strategy(self, file_extension: str) -> FileInputStrategy:
        """Returns the strategy associated with the file_extension."""
        strategy = self.strategies.get(file_extension)
        if not strategy:
            msg = f"Unsupported file extension: {file_extension}"
            raise ValueError(msg)
        return strategy

    def read_cards(self, file_path: str, reverse: bool = False) -> list[Card]:
        """Reads the entries at file_path."""
        path = Path(file_path)
        strategy = self.get_strategy(path.suffix.lower())
        return strategy.read_cards(path, reverse=reverse)


class DataServer:
    """This class serves the desired by the client."""

    def __init__(self) -> None:
        """Instantiates the DataServer."""
        self.file_reader = FileInputReader()

    def read_cards(self, file_path: str, reverse: bool = False) -> list[Card]:
        """Reads the entries associated with the file at file_path."""
        uri_info = urlparse(file_path)

        if uri_info.scheme in ["http", "https"]:
            data = urlopen(file_path).read()
            with tempfile.TemporaryDirectory(delete=False) as tempdir:
                filepath = Path(tempdir) / "tmp.csv"
                with filepath.open("w", encoding="utf-8") as fp:
                    fp.write(data.decode("utf-8"))
                file_path = fp.name

        try:
            return self.file_reader.read_cards(file_path, reverse=reverse)
        except FileNotFoundError as err:
            msg = f"Error: The file at path '{file_path}' was not found."
            raise FileNotFoundError(msg) from err
        except ValueError as err:
            msg = f"Error: {err}"
            raise ValueError(msg) from err

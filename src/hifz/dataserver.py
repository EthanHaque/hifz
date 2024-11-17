"""The dataserver module is responsible for serving content."""

import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path

from hifz.models import Card


class FileInputStrategy(ABC):
    """This ABC is an interface for the delivery independent of file types."""

    @abstractmethod
    def read_entries(self, file_path: Path) -> list[Card]:
        """Reads the entries from file_path."""


class CSVFileInputStrategy(FileInputStrategy):
    """This class maintains the logic for reading from csv files types."""

    def read_entries(self, file_path: Path) -> list[Card]:
        """Reads the entries from the csv at file_path."""
        with file_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [Card(e["front"], e["back"]) for e in reader]


class JSONFileInputStrategy(FileInputStrategy):
    """This class maintains the logic for reading from json files types."""

    def read_entries(self, file_path: Path) -> list[Card]:
        """Reads the entries from the json at file_path."""
        with file_path.open("r", encoding="utf-8") as f:
            entries = json.load(f)
            return [Card(e["front"], e["back"]) for e in entries]


class FileInputReader:
    """Dispatches the appropriate reader strategy based on file extension."""

    def __init__(self) -> None:
        """Instantiates the FileInputReader."""
        self.strategies = {
            ".csv": CSVFileInputStrategy(),
            ".json": JSONFileInputStrategy(),
        }

    def get_strategy(self, file_extension: str) -> FileInputStrategy:
        """Returns the strategy associated with the file_extension."""
        strategy = self.strategies.get(file_extension)
        if not strategy:
            msg = f"Unsupported file extension: {file_extension}"
            raise ValueError(msg)
        return strategy

    def read_entries(self, file_path: str) -> list[Card]:
        """Reads the entries at file_path."""
        path = Path(file_path)
        strategy = self.get_strategy(path.suffix.lower())
        return strategy.read_entries(path)


class DataServer:
    """This class serves the desired by the client."""

    def __init__(self) -> None:
        """Instantiates the DataServer."""
        self.file_reader = FileInputReader()

    def read_entries(self, file_path: str) -> list[Card]:
        """Reads the entries associated with the file at file_path."""
        try:
            return self.file_reader.read_entries(file_path)
        except FileNotFoundError as err:
            msg = f"Error: The file at path '{file_path}' was not found."
            raise FileNotFoundError(msg) from err
        except ValueError as err:
            msg = f"Error: {err}"
            raise ValueError(msg) from err

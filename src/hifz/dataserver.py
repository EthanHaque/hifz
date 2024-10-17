import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path

from hifz.models import Card


class FileInputStrategy(ABC):
    @abstractmethod
    def read_entries(self, file_path: Path) -> list[Card]:
        pass


class CSVFileInputStrategy(FileInputStrategy):
    def read_entries(self, file_path: Path) -> list[Card]:
        with file_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [Card(e["front"], e["back"]) for e in reader]


class JSONFileInputStrategy(FileInputStrategy):
    def read_entries(self, file_path: Path) -> list[Card]:
        with file_path.open("r", encoding="utf-8") as f:
            entries = json.load(f)
            return [Card(e["front"], e["back"]) for e in entries]


class FileInputReader:
    """Dispatches the appropriate reader strategy based on file extension."""

    def __init__(self) -> None:
        self.strategies = {
            ".csv": CSVFileInputStrategy(),
            ".json": JSONFileInputStrategy(),
        }

    def get_strategy(self, file_extension: str) -> FileInputStrategy:
        strategy = self.strategies.get(file_extension)
        if not strategy:
            msg = f"Unsupported file extension: {file_extension}"
            raise ValueError(msg)
        return strategy

    def read_entries(self, file_path: str) -> list[Card]:
        path = Path(file_path)
        strategy = self.get_strategy(path.suffix.lower())
        return strategy.read_entries(path)


class DataServer:
    def __init__(self) -> None:
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

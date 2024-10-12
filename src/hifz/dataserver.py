import csv
import json
from pathlib import Path

from hifz.models import Card


class DataServer:
    def read_entries(self, file_path: str) -> list[Card]:
        """Reads the entries associatied with the csv at file_path.

        Args:
            file_path (str): The file path of the csv.

        Returns:
            list[Card]: The list of cards.
        """
        cards = []

        try:
            with Path(file_path).open() as f:
                if file_path.lower.endswith(".csv"):
                    entries = csv.DictReader(f)
                elif file_path.endswith(".json"):
                    entries = json.load(f)
                cards = [Card(e["front"], e["back"]) for e in entries]
        except FileNotFoundError as err:
            error_message = f"Error: The file at path '{file_path}' was not found."
            raise FileNotFoundError(error_message) from err

        return cards

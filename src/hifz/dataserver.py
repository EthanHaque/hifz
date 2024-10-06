import csv
from pathlib import Path

from utils import Card


class DataServer:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self._cards = self.__read_file()  # Read the file during initialization

    def __read_file(self) -> list[Card]:
        """Private helper method to read the file and store the data."""
        cards = []

        try:
            with Path(self.file_name).open() as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    cards.append(Card(*row))
        except FileNotFoundError:
            raise f"Error: The file '{self.file_name}' was not found." from None

        return cards

    def get_cards(self) -> list[Card]:
        """Returns the list of tuples."""
        return self._cards

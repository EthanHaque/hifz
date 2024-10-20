"""This initializes the visualizers package."""

from abc import ABC, abstractmethod

from hifz.card_engine import CardEngine


class CardInterface(ABC):
    """This ABC represents the CardInterface."""

    @abstractmethod
    def display_card_front(self, card: Card) -> None:
        """Displays the card front."""

    @abstractmethod
    def display_card_back(self, card: Card) -> None:
        """Displays the card back."""

    @abstractmethod
    def notify(self, message: str) -> None:
        """Notifies with a message."""

    @abstractmethod
    def run_session(self, engine: CardEngine) -> None:
        """Runs the session."""

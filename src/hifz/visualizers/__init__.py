"""This initializes the visualizers package."""

from abc import ABC, abstractmethod

from hifz.card_engine import CardEngine
from hifz.models import Card


class Visualizer(ABC):
    """Interface for the visualizers."""

    @abstractmethod
    def display_card_front(self, card: Card) -> None:
        """Displays the card front.

        Args:
            card (Card): The card to display.
        """

    @abstractmethod
    def display_card_back(self, card: Card) -> None:
        """Displays the card back.

        Args:
            card (Card): The card to display.
        """

    @abstractmethod
    def notify(self, message: str) -> None:
        """Notifies the user with message.

        Args:
            message (str): The message to notify the user.
        """

    @abstractmethod
    def run_session(self, engine: CardEngine) -> None:
        """Runs the session.

        Args:
            engine (CardEngine): The engine relevant to starting the session.
        """

    @abstractmethod
    def display_statistics(self, engine: CardEngine) -> None:
        """Displays the statistics for the user.

        Args:
            engine (CardEngine): The engine relevant to the session.
        """

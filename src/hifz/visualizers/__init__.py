"""This initializes the visualizers package."""

from abc import ABC, abstractmethod

from hifz.card_engine import CardEngine
from hifz.models import Card


class Visualizer(ABC):
    """Interface for the visualizers."""

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

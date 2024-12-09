"""This initializes the visualizers package."""

from abc import ABC, abstractmethod

from hifz.card_engine import CardEngine


class CardInterface(ABC):
    """This ABC represents the CardInterface."""

    @abstractmethod
    def run_session(self, engine: CardEngine) -> None:
        """Runs the session."""

    @abstractmethod
    def display_statistics(self, engine: CardEngine) -> None:
        """Computes the global statistics and displays a representation to be displayed to the user."""

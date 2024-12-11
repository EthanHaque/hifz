"""This initializes the visualizers package."""

from abc import ABC, abstractmethod

from hifz.card_engine import CardEngine


class Visualizer(ABC):
    """Interface for the visualizers."""

    @abstractmethod
    def run_session(self, engine: CardEngine) -> None:
        """Runs the session.

        Args:
            engine (CardEngine): The engine relevant to starting the session.
        """

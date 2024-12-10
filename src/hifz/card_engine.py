"""The card engine maintains the logic associated with user interaction and content production."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hifz.dataserver import DataServer
from hifz.learning_strategies import CardStrategy
from hifz.models import Card, Feedback
from hifz.utils import CardSession


@dataclass
class CardEngine:
    """This class is responsible for running the main Hifz program."""

    strategy: CardStrategy

    def __post_init__(self) -> None:
        """Instantiates the CardEngine."""
        self.session: CardSession

    def get_next_card(self) -> Card:
        """Returns the next card.

        Returns:
            Card: The next card.
        """
        return self.session.get_next_card()

    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Processes the user feedback.

        Args:
            card (Card): The card associated with the feedback.
            feedback (Feedback): The user feedback associated with the card.
        """
        self.session.strategy.process_feedback(card, feedback)

    def get_feedback(self) -> Feedback:
        """Returns the feedback for the visualizer.

        Returns:
            Feedback: The feedback object for the visualizer.
        """
        return self.session.strategy.create_feedback()

    def load_cards(self, file_path: str, reverse: bool = False) -> bool:
        """Loads the cards at file_path to be interacted with.

        Args:
            file_path (str): The file_path of the cards.

        Returns:
            bool: Whether the retrieval was successful.
        """
        data_server = DataServer()
        try:
            new_cards = data_server.read_entries(file_path, reverse=reverse)
            self.session = CardSession(new_cards, self.strategy)
            return True
        except Exception:
            return False

    def save_progress(self, file_path: Path) -> None:
        """Saves the current session state.

        Args:
            file_path (Path): The file path to save the state.
        """
        self.session.save_progress(file_path)

    def load_progress(self, file_path: Path) -> None:
        """Loads progress associated with the file path.

        Args:
            file_path (Path): The file path to load the progress from.
        """
        self.session = CardSession.load_progress(file_path)
        self.strategy = self.session.strategy  # TODO: bad hack.

    def get_statistics(self) -> dict[str, Any]:
        """Returns the associated with the session.

        Returns:
            dict[str, Any]: The statistics associated with the session.
        """
        return self.session.get_statistics()

    def __str__(self) -> str:
        """Human-readable representation of the CardEngine."""
        return (
            f"{self.__class__.__name__}(strategy={self.strategy.__class__.__name__}, "
            f"cards_loaded={len(self.session.cards) if hasattr(self, 'session') else 0})"
        )

    def __repr__(self) -> str:
        """Detailed technical representation of the CardEngine."""
        return (
            f"{self.__class__.__name__}("
            f"strategy={self.strategy!r}, "
            f"session={repr(self.session) if hasattr(self, 'session') else None})"
        )

"""The card engine maintains the logic associated with user interaction and content production."""

from pathlib import Path
from typing import Any

from hifz.dataserver import DataServer
from hifz.learning_strategies import CardStrategy
from hifz.models import Card, Feedback
from hifz.utils import CardSession


class CardEngine:
    """This class is responsible for running the main Hifz program."""

    def __init__(self, strategy: CardStrategy) -> None:
        """Instantiates the CardEngine."""
        self.session: CardSession
        self.strategy = strategy

    def get_next_card(self) -> Card:
        """Returns the next card."""
        return self.session.next_card()

    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Processes the user feedback."""
        self.session.strategy.process_feedback(card, feedback)

    def get_feedback(self) -> Feedback:
        """Gets the feedback type for the particular strategy used."""
        return self.session.strategy.create_feedback()

    def load_cards(self, file_path: str) -> bool:
        """Loads the cards at file_path to be interacted with."""
        data_server = DataServer()
        try:
            new_cards = data_server.read_entries(file_path)
            self.session = CardSession(new_cards, self.strategy)
            return True
        except Exception:
            return False

    def reload_cards(self, file_path: str) -> bool:
        """Reloads the cards at file_path."""
        return self.load_cards(file_path)

    def save_progress(self, file_path: Path) -> None:
        """Saves the current session state."""
        self.session.save_progress(file_path)

    def load_progress(self, file_path: Path) -> None:
        """Loads a session from saved progress."""
        self.session = CardSession.load_progress(file_path)
        self.strategy = self.session.strategy  # TODO: bad hack.

    def aggregate_statistics(self) -> dict[str, Any]:
        """Gets global statistics from the CardSession."""
        return self.session.aggregate_statistics()

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

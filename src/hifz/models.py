"""This represents data models for the application."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Feedback:
    """This class maintains dynamic user feedback."""

    data: dict[str, Any] = field(default_factory=dict)

    def add(self, key: str, value: Any) -> None:
        """Add a key-value pair to the feedback data."""
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the feedback data."""
        return self.data.get(key, default)


@dataclass
class CardPerformance:
    """This class maintains the logic associated with recording card performance."""

    correct_guesses: int = 0
    incorrect_guesses: int = 0

    def record_correct(self) -> None:
        """Records a correct card guess."""
        self.correct_guesses += 1

    def record_incorrect(self) -> None:
        """Records an incorrect card guess."""
        self.incorrect_guesses += 1


@dataclass
class Card:
    """This class wraps logic associated with a card."""

    front: str
    back: str
    performance: CardPerformance = field(default_factory=CardPerformance)

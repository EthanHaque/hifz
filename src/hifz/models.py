from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class Feedback:
    data: Dict[str, Any] = field(default_factory=dict)

    def add(self, key: str, value: Any) -> None:
        """Add a key-value pair to the feedback data."""
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the feedback data."""
        return self.data.get(key, default)

@dataclass
class CardPerformance:
    correct_guesses: int = 0
    incorrect_guesses: int = 0

    def record_correct(self):
        self.correct_guesses += 1

    def record_incorrect(self):
        self.incorrect_guesses += 1

@dataclass
class Card:
    front: str
    back: str
    performance: CardPerformance = field(default_factory=CardPerformance)

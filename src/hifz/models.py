"""This represents data models for the application."""

from collections.abc import Callable
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
class FeedbackSummary:
    """Aggregates arbitrary feedback over time."""

    data: dict[str, Any] = field(default_factory=dict)

    def update(
        self, key: str, value: Any, update_function: Callable[[Any, Any], Any]
    ) -> None:
        """Updates the value associated with a key using the provided update function.

        Args:
            key (str): The key in the dictionary.
            value (Any): The new value to incorporate.
            update_function (Callable[[Any, Any], Any]): The function to combine existing and new values.
        """
        current_value = self.data.get(key, None)
        self.data[key] = update_function(current_value, value)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the feedback data."""
        return self.data.get(key, default)


@dataclass(frozen=True, eq=True)
class Card:
    """This class wraps logic associated with a card."""

    front: str
    back: str

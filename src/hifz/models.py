"""This represents data models for the application."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Feedback(ABC):
    """Base class for feedback with dynamic metadata."""

    data: dict[str, Any] = field(default_factory=dict)

    @abstractmethod
    def get_metadata(self) -> dict[str, dict[str, Any]]:
        """Returns metadata for rendering feedback UI."""

    def validate(self) -> None:
        """Ensures the feedback data matches its metadata."""
        metadata = self.get_metadata()
        for field_name, meta in metadata.items():
            value = self.data.get(field_name)
            if not isinstance(value, meta["type"]):
                msg = f"Field '{field_name}' must be of type {meta['type']}."
                raise TypeError(msg)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the feedback data."""
        return self.data.get(key, default)


@dataclass
class BinaryFeedback(Feedback):
    """Feedback that allows a single option to be True or False."""

    def __init__(self, field_name: str) -> None:
        """Initialize the feedback with a single boolean field."""
        super().__init__()
        self.field_name = field_name
        self.data = {field_name: False}

    def validate(self) -> None:
        """Ensures typing is correct and the value is boolean."""
        super().validate()
        true_count = sum(self.data.values())
        if true_count > 1:
            msg = f"{self.__class__.__name__} can only have one value (True/False)."
            raise ValueError(msg)

    def get_metadata(self) -> dict[str, dict[str, Any]]:
        """Generates metadata for the single boolean option."""
        return {self.field_name: {"type": bool}}


@dataclass
class SingleSelectBooleanFeedback(Feedback):
    """Feedback that allows only one boolean field to be True."""

    def __init__(self, *options: str) -> None:
        """Initialize the feedback with multiple boolean fields."""
        super().__init__()
        self.options = options
        self.data = {option: False for option in self.options}

    def validate(self) -> None:
        """Ensures typing is correct and only one field is True."""
        super().validate()
        true_count = sum(self.data.values())
        if len(self.options) == 0:
            msg = f"No options provided for {self.__class__.__name__}."
            raise ValueError(msg)
        if true_count != 1:
            msg = f"Exactly one field must be True in {self.__class__.__name__}."
            raise ValueError(msg)

    def get_metadata(self) -> dict[str, dict[str, Any]]:
        """Generates metadata for the multiple boolean options."""
        return {option: {"type": bool} for option in self.options}


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


@dataclass
class Card:
    """This class wraps logic associated with a card."""

    front: str
    back: str
    statistics: FeedbackSummary = field(default_factory=FeedbackSummary)

    def to_dict(self) -> dict[str, Any]:
        """Converts the card and its statistics to a dictionary."""
        return {
            "front": self.front,
            "back": self.back,
            "statistics": self.statistics.data,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Card":
        """Creates a Card instance from a dictionary."""
        card = cls(front=data["front"], back=data["back"])
        card.statistics.data = data.get("statistics", {})
        return card

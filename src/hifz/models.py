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
class SingleSelectBooleanFeedback(Feedback):
    """Feedback that allows only one boolean field to be True."""

    def __init__(self, *options: str) -> None:
        """Initialize the feedback with arbitrary boolean fields."""
        super().__init__()
        self.options = options
        self.data = {option: False for option in self.options}

    def validate(self) -> None:
        """Ensures only one field is True."""
        super().validate()
        true_count = sum(self.data.values())
        num_options = len(self.options)
        if num_options == 0:
            msg = "No values in feedback object"
            raise ValueError(msg)
        if true_count != 1 and num_options > 1:
            msg = "Only one field can be True."
            raise ValueError(msg)
        if (true_count != 0 and true_count != 1) and num_options == 1:
            msg = "There was only a single option, but we counted an incorrect number of responses."
            raise ValueError(msg)

    def get_metadata(self) -> dict[str, dict[str, Any]]:
        """Generates metadata for the provided options."""
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

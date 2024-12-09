"""This module maintains the strategies associated with order of card display."""

import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any

from hifz.models import BinaryFeedback, Card, Feedback

STRATEGY_NAME_TO_CLASS: dict[str, type["CardStrategy"]] = {}
STRATEGY_CLASS_TO_NAME: dict[type["CardStrategy"], str] = {}


def register_strategy(name: str):
    """Decorator to register a strategy with a two-way mapping."""

    def decorator(cls):
        if name in STRATEGY_NAME_TO_CLASS or cls in STRATEGY_CLASS_TO_NAME:
            msg = f"Strategy name '{name}' or class '{cls.__name__}' is already registered."
            raise ValueError(msg)
        STRATEGY_NAME_TO_CLASS[name] = cls
        STRATEGY_CLASS_TO_NAME[cls] = name
        return cls

    return decorator


class CardStrategy(ABC):
    """Interface for card memorization strategies."""

    @abstractmethod
    def get_next_card(self, cards: list[Card]) -> Card:
        """Returns the next card."""

    @abstractmethod
    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Processes the feedback associated with the card."""

    @abstractmethod
    def create_feedback(self) -> Feedback:
        """Defines the type of feedback the strategy uses."""

    @abstractmethod
    def aggregate_statistics(self, cards: list[Card]) -> dict[str, Any]:
        """Computes global statistics."""

    def to_dict(self) -> dict[str, Any]:
        """Serializes the strategy state."""
        strategy_name = STRATEGY_CLASS_TO_NAME.get(type(self))
        if not strategy_name:
            msg = f"Strategy class {type(self).__name__} is not registered."
            raise ValueError(msg)
        return {
            "type": strategy_name,
            "state": self._serialize_state(),
        }

    def _serialize_state(self) -> dict[str, Any]:
        """Hook for subclasses to serialize additional state."""
        return {}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CardStrategy":
        """Restores the strategy state."""
        if "type" not in data:
            msg = "Missing 'type' in serialized data."
            raise KeyError(msg)
        if "state" not in data:
            msg = "Missing 'state' in serialized data."
            raise KeyError(msg)

        strategy_name = data["type"]
        strategy_cls = STRATEGY_NAME_TO_CLASS.get(strategy_name)
        if not strategy_cls:
            msg = f"Unknown strategy name: {strategy_name}"
            raise ValueError(msg)

        return strategy_cls._deserialize_state(data["state"])

    @classmethod
    def _deserialize_state(cls, state: dict[str, Any]) -> "CardStrategy":
        """Hook for subclasses to deserialize additional state."""
        _ = state
        return cls()

    def __repr__(self) -> str:
        """Machine-readable representation of the strategy."""
        return f"<{self.__class__.__name__} {self._serialize_state()}>"

    def __str__(self) -> str:
        """User-friendly string representation of the strategy."""
        state = self._serialize_state()
        state_details = ", ".join(f"{key}={value}" for key, value in state.items())
        return f"{self.__class__.__name__}({state_details})"


@register_strategy("RandomStrategy")
class RandomStrategy(CardStrategy):
    """This class offers a random ordering of the cards."""

    def get_next_card(self, cards: list[Card]) -> Card:
        """Returns the next card."""
        return random.choice(cards)

    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Processes the feedback associated with the card."""
        feedback.validate()
        card.statistics.update(
            key="correct",
            value=1 if feedback.get("correct") else 0,
            update_function=lambda existing, new: (existing or 0) + new,
        )
        card.statistics.update(
            key="incorrect",
            value=0 if feedback.get("correct") else 1,
            update_function=lambda existing, new: (existing or 0) + new,
        )

    def create_feedback(self) -> Feedback:
        """Gets the type of Feedback this strategy uses."""
        return BinaryFeedback("correct")

    def aggregate_statistics(self, cards: list[Card]) -> dict[str, Any]:
        """Computes total number of correct and incorrect."""
        total_correct = 0
        total_incorrect = 0
        for card in cards:
            total_correct += card.statistics.get(key="correct", default=0)
            total_incorrect += card.statistics.get(key="incorrect", default=0)
        return {"Correct": total_correct, "Incorrect": total_incorrect}


@register_strategy("SequentialStrategy")
class SequentialStrategy(CardStrategy):
    """This class represents the logic associated with providing a sequential ordering of cards."""

    def __init__(self) -> None:
        """Instantiates the Sequential Strategy."""
        self.index = 0

    def get_next_card(self, cards: list[Card]) -> Card:
        """Returns the next card."""
        card = cards[self.index]
        self.index = (self.index + 1) % len(cards)
        return card

    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Processes the feedback associated with the card."""
        feedback.validate()
        card.statistics.update(
            key="correct",
            value=1 if feedback.get("correct") else 0,
            update_function=lambda existing, new: (existing or 0) + new,
        )
        card.statistics.update(
            key="incorrect",
            value=0 if feedback.get("correct") else 1,
            update_function=lambda existing, new: (existing or 0) + new,
        )

    def create_feedback(self) -> Feedback:
        """Gets the type of Feedback this strategy uses."""
        return BinaryFeedback("correct")

    def aggregate_statistics(self, cards: list[Card]) -> dict[str, Any]:
        """Placeholder."""
        global_statistics = {}
        for card in cards:
            global_statistics[card.front] = card.statistics
        return global_statistics


@register_strategy("MasteryStrategy")
class MasteryStrategy(CardStrategy):
    """This class maintains the logic associated with a card ordering for mastery learning."""

    def __init__(self, threshold: int = 5) -> None:
        """Instantiates the Mastery Strategy with a configurable mastery threshold."""
        self.index = 0
        self.threshold = threshold

    def get_next_card(self, cards: list[Card]) -> Card:
        """Returns the next card, prioritizing those below the mastery threshold."""
        low_mastery_cards = [
            card
            for card in cards
            if card.statistics.data.get("correct", 0) < self.threshold
        ]

        if low_mastery_cards:
            card = low_mastery_cards[self.index % len(low_mastery_cards)]
            self.index = (self.index + 1) % len(low_mastery_cards)
        else:
            card = cards[self.index % len(cards)]
            self.index = (self.index + 1) % len(cards)
        return card

    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Processes the feedback associated with the card."""
        feedback.validate()

        if feedback.get("correct"):
            card.statistics.update(
                key="correct",
                value=1,
                update_function=lambda existing, new: (existing or 0) + new,
            )
        else:
            card.statistics.update(
                key="correct",
                value=0,
                update_function=lambda _, new: new,
            )

        card.statistics.update(
            key="seen",
            value=1,
            update_function=lambda existing, new: (existing or 0) + new,
        )

    def create_feedback(self) -> Feedback:
        """Gets the type of Feedback this strategy uses."""
        return BinaryFeedback("correct")

    def aggregate_statistics(self, cards: list[Card]) -> dict[str, Any]:
        """Placeholder."""
        global_statistics = {}
        for card in cards:
            global_statistics[card.front] = card.statistics
        return global_statistics

    def _serialize_state(self) -> dict[str, Any]:
        """Serializes the strategy state."""
        return {"index": self.index, "threshold": self.threshold}

    @classmethod
    def _deserialize_state(cls, data: dict[str, Any]) -> "MasteryStrategy":
        """Restores the strategy state."""
        instance = cls(threshold=data.get("threshold", 5))
        instance.index = data.get("index", 0)
        return instance


@register_strategy("SimpleSpacedRepetitionStrategy")
class SimpleSpacedRepetitionStrategy(CardStrategy):
    """This class implements a simple spaced repetition algorithm."""

    def get_next_card(self, cards: list[Card]) -> Card:
        """Returns the next card to review based on due time.

        Args:
            cards (List[Card]): List of all available cards.

        Returns:
            Card: The next card to review.
        """
        now = datetime.now()
        sorted_cards = sorted(
            cards, key=lambda card: card.statistics.data.get("due", now)
        )

        for card in sorted_cards:
            due = card.statistics.data.get("due", now)
            if due <= now:
                return card

        return random.choice(cards)

    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Process feedback and schedule the next review.

        Args:
            card (Card): The card being reviewed.
            feedback (Feedback): The feedback provided by the user.
        """
        feedback.validate()
        card.statistics.update(
            key="correct",
            value=1 if feedback.get("correct") else 0,
            update_function=lambda existing, new: (existing or 0) + new,
        )
        card.statistics.update(
            key="incorrect",
            value=0 if feedback.get("correct") else 1,
            update_function=lambda existing, new: (existing or 0) + new,
        )

        ease_factor = card.statistics.data.get("ease_factor", 2.5)

        if feedback.get("correct"):
            interval = card.statistics.data.get("interval", 1)
            card.statistics.update(
                key="interval",
                value=interval * ease_factor,
                update_function=lambda existing, new: max(existing or 1, new),
            )
            card.statistics.update(
                key="ease_factor",
                value=ease_factor + 0.1,
                update_function=lambda _, new: min(new, 3.0),
            )
        else:
            card.statistics.update(
                key="interval", value=1, update_function=lambda _, new: new
            )
            card.statistics.update(
                key="ease_factor",
                value=max(ease_factor - 0.2, 1.3),
                update_function=lambda _, new: new,
            )

        next_due = datetime.now() + timedelta(days=card.statistics.data["interval"])
        card.statistics.update(
            key="due", value=next_due, update_function=lambda _, new: new
        )

    def create_feedback(self) -> Feedback:
        """Defines the type of feedback this strategy uses."""
        return BinaryFeedback("correct")

    def aggregate_statistics(self, cards: list[Card]) -> dict[str, Any]:
        """Placeholder."""
        global_statistics = {}
        for card in cards:
            global_statistics[card.front] = card.statistics
        return global_statistics

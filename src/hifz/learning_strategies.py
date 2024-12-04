"""This module maintains the strategies associated with order of card display."""

import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from hifz.models import Card, Feedback, SingleSelectBooleanFeedback


class CardStrategy(ABC):
    """This ABC offers the interface associated with card display order strategy."""

    @abstractmethod
    def get_next_card(self, cards: list[Card]) -> Card:
        """Returns the next card."""

    @abstractmethod
    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Processes the feedback associated with the card."""

    @abstractmethod
    def create_feedback(self) -> Feedback:
        """Defines the type of feedback the strategy recieves from the visualizer."""


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
        return SingleSelectBooleanFeedback("correct")


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
        return SingleSelectBooleanFeedback("correct")


class MasteryStrategy(CardStrategy):
    """This class maintains the logic associated with a card ordering for mastery learning."""

    def __init__(self) -> None:
        """Instantiates the Mastery Strategy."""
        self.index = 0

    def get_next_card(self, cards: list[Card]) -> Card:
        """Returns the next card."""
        threshold = 5

        start_index = self.index
        while True:
            card = cards[self.index]
            if card.statistics.data.get("correct", 0) < threshold:
                self.index = (self.index + 1) % len(cards)
                return card

            self.index = (self.index + 1) % len(cards)

            if self.index == start_index:
                break

        self.index = (self.index + 1) % len(cards)
        return cards[self.index]

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
        return SingleSelectBooleanFeedback("correct")


class SimpleSpacedRepetition(CardStrategy):
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
        return SingleSelectBooleanFeedback("correct")

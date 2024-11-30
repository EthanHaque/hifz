"""This module maintains the strategies associated with order of card display."""

import random
from abc import ABC, abstractmethod

from hifz.models import Card, Feedback


class CardStrategy(ABC):
    """This ABC offers the interface associated with card display order strategy."""

    @abstractmethod
    def get_next_card(self, cards: list[Card]) -> Card:
        """Returns the next card."""

    @abstractmethod
    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Processes the feedback associated with the card."""


class RandomStrategy(CardStrategy):
    """This class offers a random ordering of the cards."""

    def get_next_card(self, cards: list[Card]) -> Card:
        """Returns the next card."""
        return random.choice(cards)

    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Processes the feedback associated with the card."""
        if feedback.get("correct"):
            card.performance.record_correct()
        else:
            card.performance.record_incorrect()


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
        if feedback.get("correct"):
            card.performance.record_correct()
        else:
            card.performance.record_incorrect()


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
            if card.performance.correct_guesses < threshold:
                self.index = (self.index + 1) % len(cards)
                return card

            self.index = (self.index + 1) % len(cards)

            if self.index == start_index:
                break

        self.index = (self.index + 1) % len(cards)
        return cards[self.index]

    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        """Processes the feedback associated with the card."""
        if feedback.get("correct"):
            card.performance.record_correct()
        else:
            card.performance.correct_guesses = 0

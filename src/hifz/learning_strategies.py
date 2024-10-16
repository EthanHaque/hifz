import random
from abc import ABC, abstractmethod

from hifz.models import Card, Feedback


class CardStrategy(ABC):
    @abstractmethod
    def get_next_card(self, cards: list[Card]) -> Card:
        pass

    @abstractmethod
    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        pass


class RandomStrategy(CardStrategy):
    def get_next_card(self, cards: list[Card]) -> Card:
        return random.choice(cards)

    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        if feedback.get("correct"):
            card.performance.record_correct()
        else:
            card.performance.record_incorrect()


class SequentialStrategy(CardStrategy):
    def __init__(self):
        self.index = 0

    def get_next_card(self, cards: list[Card]) -> Card:
        card = cards[self.index]
        self.index = (self.index + 1) % len(cards)
        return card

    def process_feedback(self, card: Card, feedback: Feedback) -> None:
        if feedback.get("correct"):
            card.performance.record_correct()
        else:
            card.performance.record_incorrect()


class MasteryStrategy(CardStrategy):
    def __init__(self):
        self.index = 0

    def get_next_card(self, cards: list[Card]) -> Card:
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
        if feedback.get("correct"):
            card.performance.record_correct()
        else:
            card.performance.correct_guesses = 0

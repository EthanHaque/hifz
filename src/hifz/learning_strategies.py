import random
from abc import ABC, abstractmethod

from hifz.models import Card


class FlashcardStrategy(ABC):
    @abstractmethod
    def get_next_flashcard(self, flashcards: list[Card]) -> Card:
        pass


class RandomStrategy(FlashcardStrategy):
    def get_next_flashcard(self, flashcards: list[Card]) -> Card:
        return random.choice(flashcards)


class SequentialStrategy(FlashcardStrategy):
    def __init__(self):
        self.index = 0

    def get_next_flashcard(self, flashcards: list[Card]) -> Card:
        card = flashcards[self.index]
        self.index = (self.index + 1) % len(flashcards)
        return card

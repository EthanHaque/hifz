import random
from abc import ABC, abstractmethod

from utils import Card


class FlashcardStrategy(ABC):
    @abstractmethod
    def get_next_flashcard(self, flashcards: list[Card]) -> Card:
        pass


class RandomStrategy(FlashcardStrategy):
    def get_next_flashcard(self, flashcards: list[Card]) -> Card:
        return random.choice(flashcards)

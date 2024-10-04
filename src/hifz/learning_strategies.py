from abc import ABC, abstractmethod

from utils import Card


class FlashcardStrategy(ABC):
    @abstractmethod
    def get_next_flashcard(self, flashcards) -> Card:
        pass

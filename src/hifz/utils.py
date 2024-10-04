from hifz.learning_strategies import FlashcardStrategy
from hifz.models import Card


class FlashcardSession:
    def __init__(self, flashcards: list[Card], strategy: FlashcardStrategy):
        self.flashcards = flashcards
        self.strategy = strategy

    def next_flashcard(self) -> Card:
        return self.strategy.get_next_flashcard(self.flashcards)

from hifz.learning_strategies import RandomStrategy, SequentialStrategy
from hifz.models import Card
from hifz.utils import FlashcardSession


def test_flashcard_session_with_random_strategy(flashcards: list[Card]):
    random_strategy = RandomStrategy()
    session = FlashcardSession(flashcards, random_strategy)
    card = session.next_flashcard()
    assert card in flashcards


def test_flashcard_session_with_sequential_strategy(flashcards: list[Card]):
    sequential_strategy = SequentialStrategy()
    session = FlashcardSession(flashcards, sequential_strategy)

    assert session.next_flashcard() == flashcards[0]
    assert session.next_flashcard() == flashcards[1]

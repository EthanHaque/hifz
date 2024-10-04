from hifz.learning_strategies import RandomStrategy, SequentialStrategy
from hifz.models import Card
from hifz.utils import FlashcardSession


def test_random_strategy_returns_card(flashcards: list[Card]):
    random_strategy = RandomStrategy()
    session = FlashcardSession(flashcards, random_strategy)
    card = session.next_flashcard()
    assert card in flashcards


def test_sequential_strategy_returns_in_order(flashcards: list[Card]):
    sequential_strategy = SequentialStrategy()
    session = FlashcardSession(flashcards, sequential_strategy)

    card1 = session.next_flashcard()
    card2 = session.next_flashcard()
    card3 = session.next_flashcard()

    assert card1 == flashcards[0]
    assert card2 == flashcards[1]
    assert card3 == flashcards[2]


def test_sequential_strategy_wraps_around(flashcards: list[Card]):
    sequential_strategy = SequentialStrategy()
    session = FlashcardSession(flashcards, sequential_strategy)

    # Loop through the list to force wrap-around
    for _ in range(len(flashcards)):
        session.next_flashcard()

    card = session.next_flashcard()
    assert card == flashcards[0], "SequentialStrategy did not wrap around."

"""This module maintains the utility models and methods for the program."""

from hifz.learning_strategies import CardStrategy
from hifz.models import Card, Feedback


class SessionStatistics:
    """This class stores the statistics associated with a CardSession to notify the user with at the end of a session."""

    def __init__(self) -> None:
        """Instantiates the SessionStatistics."""
        self.correct_answers = 0
        self.incorrect_answers = 0

    def process_feedback(self, feedback: Feedback) -> None:
        """Processes the feedback from the current card."""
        if feedback.get("correct"):
            self.correct_answers += 1
        else:
            self.incorrect_answers += 1

    def get_summary(self) -> str:
        """Returns a string with the summary to notify the user."""
        return f"Correct: {self.correct_answers}, Incorrect: {self.incorrect_answers}."


class CardSession:
    """This class maintains the logic associated with starting a Card Session."""

    def __init__(self, cards: list[Card], strategy: CardStrategy) -> None:
        """Instantiates the CardSession."""
        self.cards = cards
        self.strategy = strategy
        self.statistics = SessionStatistics()

    def next_card(self) -> Card:
        """Returns the next card."""
        return self.strategy.get_next_card(self.cards)

    def process_feedback(self, card: Card, **kwargs) -> None:
        """Processes the feedback for the current card."""
        feedback = Feedback(kwargs)
        self.strategy.process_feedback(card, feedback)
        self.statistics.process_feedback(feedback)

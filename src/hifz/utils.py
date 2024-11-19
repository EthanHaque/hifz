from hifz.learning_strategies import CardStrategy
from hifz.models import Card, Feedback


class SessionStatistics:
    def __init__(self) -> None:
        self.correct_answers = 0
        self.incorrect_answers = 0

    def process_feedback(self, feedback: Feedback) -> None:
        if feedback.get("correct"):
            self.correct_answers += 1
        else:
            self.incorrect_answers += 1

    def get_summary(self) -> str:
        return f"Correct: {self.correct_answers}, Incorrect: {self.incorrect_answers}."


class CardSession:
    def __init__(self, cards: list[Card], strategy: CardStrategy) -> None:
        self.cards = cards
        self.strategy = strategy
        self.statistics = SessionStatistics()

    def next_card(self) -> Card:
        return self.strategy.get_next_card(self.cards)

    def process_feedback(self, card: Card, **kwargs) -> None:
        feedback = Feedback(kwargs)
        self.strategy.process_feedback(card, feedback)
        self.statistics.process_feedback(feedback)

    def get_summary(self) -> str:
        return self.statistics.get_summary()

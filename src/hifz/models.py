from dataclasses import dataclass, field


@dataclass
class CardPerformance:
    correct_guesses: int = 0
    incorrect_guesses: int = 0

    def record_correct(self):
        self.correct_guesses += 1

    def record_incorrect(self):
        self.incorrect_guesses += 1


@dataclass
class Card:
    front: str
    back: str
    performance: CardPerformance = field(default_factory=CardPerformance)

from hifz.learning_strategies import CardStrategy
from hifz.models import Card


class CardSession:
    def __init__(self, cards: list[Card], strategy: CardStrategy):
        self.cards = cards
        self.strategy = strategy

    def next_card(self) -> Card:
        return self.strategy.get_next_card(self.cards)

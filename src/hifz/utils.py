"""This module maintains the utility models and methods for the program."""

from hifz.learning_strategies import CardStrategy
from hifz.models import Card


class CardSession:
    """This class maintains the logic associated with starting a Card Session."""

    def __init__(self, cards: list[Card], strategy: CardStrategy) -> None:
        """Instantiates the CardSession."""
        self.cards = cards
        self.strategy = strategy

    def next_card(self) -> Card:
        """Returns the next card."""
        return self.strategy.get_next_card(self.cards)
      
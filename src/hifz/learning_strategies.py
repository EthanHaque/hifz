import random
from abc import ABC, abstractmethod

from hifz.models import Card


class CardStrategy(ABC):
    @abstractmethod
    def get_next_card(self, cards: list[Card]) -> Card:
        pass


class RandomStrategy(CardStrategy):
    def get_next_card(self, cards: list[Card]) -> Card:
        return random.choice(cards)


class SequentialStrategy(CardStrategy):
    def __init__(self):
        self.index = 0

    def get_next_card(self, cards: list[Card]) -> Card:
        card = cards[self.index]
        self.index = (self.index + 1) % len(cards)
        return card

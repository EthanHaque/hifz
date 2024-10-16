from abc import ABC, abstractmethod
from hifz.card_engine import CardEngine
from hifz.models import Card

class CardInterface(ABC):
    @abstractmethod
    def display_card_front(self, card: Card) -> None:
        pass

    @abstractmethod
    def display_card_back(self, card: Card) -> None:
        pass

    @abstractmethod
    def notify(self, message: str) -> None:
        pass

    @abstractmethod
    def run_session(self, engine: CardEngine) -> None:
        pass

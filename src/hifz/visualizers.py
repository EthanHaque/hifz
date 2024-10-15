from abc import ABC, abstractmethod
from hifz.models import Card

class CardInterface(ABC):
    @abstractmethod
    def display_card_front(self, card: Card) -> None:
        pass

    @abstractmethod
    def display_card_back(self, card: Card) -> None:
        pass

    @abstractmethod
    def get_user_input(self, prompt: str) -> str:
        pass

    @abstractmethod
    def notify(self, message: str) -> None:
        pass


class TUICardInterface(CardInterface):
    def display_card_front(self, card: Card) -> None:
        print(f"\nFront: {card.front}") # noqa: T201

    def display_card_back(self, card: Card) -> None:
        print(f"Back: {card.back}") # noqa: T201

    def get_user_input(self, prompt: str) -> str:
        return input(prompt)

    def notify(self, message: str) -> None:
        print(message) # noqa: T201

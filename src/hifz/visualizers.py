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
    def run_session(self, engine: "CardEngine") -> None:
        """Controls the flow of the session, interacting with the engine as needed."""


class TUICardInterface(CardInterface):
    def display_card_front(self, card: Card) -> None:
        print(f"\nFront: {card.front}")  # noqa: T201

    def display_card_back(self, card: Card) -> None:
        print(f"Back: {card.back}")  # noqa: T201

    def notify(self, message: str) -> None:
        print(message)  # noqa: T201

    def run_session(self, engine: CardEngine) -> None:
        self.notify(
            "Starting flashcard session... Type 'q' to quit, 'reload' to load new cards."
        )

        while True:
            card = engine.get_next_card()
            self.display_card_front(card)

            action = (
                input(
                    "(Press Enter to see the back, 'q' to quit, or 'reload' to switch cards): "
                )
                .strip()
                .lower()
            )
            if action == "q":
                self.notify("Exiting the session.")
                break
            if action == "reload":
                new_file_path = input("Enter the new file path: ")
                if engine.reload_cards(new_file_path):
                    self.notify(f"Successfully loaded new cards from {new_file_path}")
                else:
                    self.notify(f"Failed to load new cards from {new_file_path}")
                continue

            self.display_card_back(card)

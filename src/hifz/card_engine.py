from hifz.learning_strategies import CardStrategy
from hifz.models import Card
from hifz.utils import CardSession
from hifz.visualizers import CardInterface


class CardEngine:
    def __init__(
        self, cards: list[Card], strategy: CardStrategy, interface: CardInterface
    ):
        self.session = CardSession(cards, strategy)
        self.interface = interface

    def run(self):
        self.interface.notify("Starting flashcard session... Type 'q' to quit.")

        while True:
            card = self.session.next_card()
            self.interface.display_card_front(card)

            user_input = self.interface.get_user_input(
                "(Press Enter to see the back, or 'q' to quit): "
            ).strip()
            if user_input.lower() == "q":
                self.interface.notify("Exiting the session.")
                break

            self.interface.display_card_back(card)
            feedback = self.interface.get_user_input(
                "(Press Enter to continue, or 'q' to quit): "
            ).strip()
            if feedback.lower() == "q":
                self.interface.notify("Exiting the session.")
                break

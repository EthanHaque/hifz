"""The card engine maintains the logic associated with user interaction and content production."""

from hifz.dataserver import DataServer
from hifz.learning_strategies import CardStrategy
from hifz.models import Card, Feedback
from hifz.utils import CardSession


class CardEngine:
    """This class is responsible for running the main Hifz program."""

    def __init__(self, strategy: CardStrategy) -> None:
        """Instantiates the CardEngine."""
        self.session: CardSession
        self.strategy = strategy

    def get_next_card(self) -> Card:
        """Returns the next card."""
        return self.session.next_card()

    def process_feedback(self, card: Card, **kwargs) -> None:
        """Processes the user feedback."""
        feedback = Feedback(kwargs)
        self.session.strategy.process_feedback(card, feedback)
        self.session.statistics.process_feedback(feedback)

    def load_cards(self, file_path: str) -> bool:
        """Loads the cards at file_path to be interacted with."""
        data_server = DataServer()
        try:
            new_cards = data_server.read_entries(file_path)
            self.session = CardSession(new_cards, self.strategy)
            return True
        except Exception:
            return False

    def reload_cards(self, file_path: str) -> bool:
        """Reloads the cards at file_path."""
        return self.load_cards(file_path)

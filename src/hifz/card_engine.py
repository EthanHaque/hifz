from hifz.dataserver import DataServer
from hifz.learning_strategies import CardStrategy
from hifz.models import Card
from hifz.utils import CardSession


class CardEngine:
    def __init__(self, strategy: CardStrategy):
        self.session = None
        self.strategy = strategy

    def get_next_card(self) -> Card:
        return self.session.next_card()

    def get_feedback(self, card: Card, correct: bool):
        if self.session:
            self.session.get_feedback(card, correct)

    def load_cards(self, file_path: str) -> bool:
        data_server = DataServer()
        try:
            new_cards = data_server.read_entries(file_path)
            self.session = CardSession(new_cards, self.strategy)
            return True
        except Exception:
            return False

    def reload_cards(self, file_path: str) -> bool:
        return self.load_cards(file_path)

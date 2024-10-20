from abc import ABC, abstractmethod

from hifz.card_engine import CardEngine


class CardInterface(ABC):
    @abstractmethod
    def run_session(self, engine: CardEngine) -> None:
        pass

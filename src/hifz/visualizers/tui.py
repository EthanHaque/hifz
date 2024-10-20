from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static
from hifz.card_engine import CardEngine
from hifz.visualizers import CardInterface
from hifz.models import Card


class CardWidget(Static):
    """A widget to display cards."""

    is_front = True
    current_card: Card

    def update_card(self, card: Card) -> None:
        self.current_card = card
        self.is_front = True
        self.update(self.current_card.front)

    def flip(self) -> None:
        self.is_front = not self.is_front
        if self.is_front:
            self.update(self.current_card.front)
        else:
            self.update(self.current_card.back)


class CardApp(App):
    BINDINGS = [
        ("j", "flip_card", "Flip Card"),
        ("k", "flip_card", "Flip Card"),
        ("l", "next_card", "Next Card"),
    ]

    def __init__(self, engine: CardEngine, **kwargs) -> None:
        super().__init__(**kwargs)
        self.engine = engine

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield CardWidget()

    def action_flip_card(self) -> None:
        self.query_one(CardWidget).flip()

    def action_next_card(self) -> None:
        next_card = self.engine.get_next_card()
        self.query_one(CardWidget).update_card(next_card)

    def on_mount(self) -> None:
        self.action_next_card()


class TUICardInterface(CardInterface):
    def run_session(self, engine: CardEngine) -> None:
        CardApp(engine).run()

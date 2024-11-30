"""TUI visualizer for card application."""

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static

from hifz.card_engine import CardEngine
from hifz.models import Card
from hifz.visualizers import CardInterface


class CardWidget(Static):
    """A widget to display cards."""

    is_front = True
    current_card: Card

    def update_card(self, card: Card) -> None:
        """Changes what card is bing displayed."""
        self.current_card = card
        self.is_front = True
        self.update(self.current_card.front)

    def flip(self) -> None:
        """Shows the other side of the card."""
        self.is_front = not self.is_front
        if self.is_front:
            self.update(self.current_card.front)
        else:
            self.update(self.current_card.back)


class CardApp(App):
    """Derived class for building TUI."""

    BINDINGS = [
        ("j", "flip_card", "Flip Card"),
        ("k", "flip_card", "Flip Card"),
        ("l", "next_card", "Next Card"),
    ]

    def __init__(self, engine: CardEngine, **kwargs) -> None:
        """Constructor for the CardApp."""
        super().__init__(**kwargs)
        self.engine = engine

    def compose(self) -> ComposeResult:
        """Puts the compotents for the visualizer together."""
        yield Header()
        yield Footer()
        yield CardWidget()

    def action_flip_card(self) -> None:
        """Helper method to flip the shown card."""
        self.query_one(CardWidget).flip()

    def action_next_card(self) -> None:
        """Helper method to get the next card in the sequence."""
        next_card = self.engine.get_next_card()
        self.query_one(CardWidget).update_card(next_card)

    def on_mount(self) -> None:
        """Gets a card as soon as the TUI loads."""
        self.action_next_card()


class TUICardInterface(CardInterface):
    """Wrapper class to conform to the CardInterface API."""

    def run_session(self, engine: CardEngine) -> None:
        """Runs the TUI visualizer."""
        CardApp(engine).run()

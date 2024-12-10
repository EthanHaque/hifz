"""TUI visualizer for card application."""

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static

from hifz.card_engine import CardEngine
from hifz.models import BinaryFeedback, Card
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

    def get_card(self) -> Card:
        """Returns the current card."""
        return self.current_card

    def flip(self) -> None:
        """Shows the other side of the card."""
        self.is_front = not self.is_front
        if self.is_front:
            self.update(self.current_card.front)
        else:
            self.update(self.current_card.back)


class CardApp(App):
    """Derived class for building TUI."""

    CSS = """
    Screen {
        align: center middle;
    }

    #card {
        background: blue 50%;
        border: wide white;
        width: 40;
        height: 9;
        text-align: center;
        content-align: center middle;
    }
    """

    BINDINGS = [
        ("j", "flip_card", "Flip Card"),
        ("k", "flip_card", "Flip Card"),
        ("u", "record_correct", "Correct"),
        ("i", "record_incorrect", "Incorrect"),
    ]

    def __init__(self, engine: CardEngine, **kwargs) -> None:
        """Constructor for the CardApp."""
        super().__init__(**kwargs)
        self.engine = engine

    def compose(self) -> ComposeResult:
        """Puts the compotents for the visualizer together."""
        yield Header()
        yield Footer()
        yield CardWidget(id="card")

    def action_flip_card(self) -> None:
        """Helper method to flip the shown card."""
        self.query_one(CardWidget).flip()

    def action_next_card(self) -> None:
        """Helper method to get the next card in the sequence."""
        next_card = self.engine.get_next_card()
        self.query_one(CardWidget).update_card(next_card)

    def action_record_correct(self) -> None:
        """Records a card as correct for BinaryFeedback."""
        feedback = self.engine.get_feedback()
        if not isinstance(feedback, BinaryFeedback):
            raise NotImplementedError()
        feedback.data[feedback.field_name] = True
        self.engine.process_feedback(self.query_one(CardWidget).get_card(), feedback)
        self.action_next_card()

    def action_record_incorrect(self) -> None:
        """Records a card as incorrect for BinaryFeedback."""
        feedback = self.engine.get_feedback()
        if not isinstance(feedback, BinaryFeedback):
            raise NotImplementedError()
        feedback.data[feedback.field_name] = False
        self.engine.process_feedback(self.query_one(CardWidget).get_card(), feedback)
        self.action_next_card()

    def on_mount(self) -> None:
        """Gets a card as soon as the TUI loads."""
        self.action_next_card()


class TUICardInterface(CardInterface):
    """Wrapper class to conform to the CardInterface API."""

    def run_session(self, engine: CardEngine) -> None:
        """Runs the TUI visualizer."""
        CardApp(engine).run()

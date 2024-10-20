from hifz.card_engine import CardEngine
from hifz.models import Card
from hifz.visualizers import CardInterface
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class StopwatchApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


class TUICardInterface(CardInterface):
    def display_card_front(self, card: Card) -> None:
        pass

    def display_card_back(self, card: Card) -> None:
        pass

    def notify(self, message: str) -> None:
        pass

    def run_session(self, engine: CardEngine) -> None:
        app = StopwatchApp()
        app.run()

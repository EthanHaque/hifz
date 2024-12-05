"""This represents the command-line interface."""

from hifz.card_engine import CardEngine
from hifz.models import Card
from hifz.visualizers import CardInterface


class CLICardInterface(CardInterface):
    """This represents the command-line interface."""

    def display_card_front(self, card: Card) -> None:
        """Displays the card front."""
        print(f"\nFront: {card.front}")  # noqa: T201

    def display_card_back(self, card: Card) -> None:
        """Displays the card back."""
        print(f"Back: {card.back}")  # noqa: T201

    def notify(self, message: str) -> None:
        """Notifies with message."""
        print(message)  # noqa: T201

    def run_session(self, engine: CardEngine) -> None:
        """Runs the session."""
        self.notify(
            "Starting flashcard session... Type 'q' to quit, 'reload' to load new cards."
        )

        while True:
            card = engine.get_next_card()
            self.display_card_front(card)

            action = (
                input(
                    "(Press Enter to see the back, 'q' to quit, 'reload' to switch cards): "
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

            correct = input("Did you get it correct? (y/n): ").strip().lower() == "y"
            engine.process_feedback(card, correct=correct)

        # Print summary of session statistics
        self.notify("-" * 69 + "\nSession Summary:")
        self.notify(engine.session.statistics.get_summary())

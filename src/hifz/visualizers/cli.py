"""This represents the command-line interface."""

from hifz.card_engine import CardEngine
from hifz.models import BinaryFeedback, Card, Feedback, SingleSelectBooleanFeedback
from hifz.visualizers import Visualizer


class CLIVisualizer(Visualizer):
    """This represents the command-line interface."""

    def display_card_front(self, card: Card) -> None:
        """Displays the card front.

        Args:
            card (Card): The card to display.
        """
        print(f"\nFront: {card.front}")  # noqa: T201

    def display_card_back(self, card: Card) -> None:
        """Displays the card back.

        Args:
            card (Card): The card to display.
        """
        print(f"Back: {card.back}")  # noqa: T201

    def notify(self, message: str) -> None:
        """Notifies the user with message.

        Args:
            message (str): The message to notify the user.
        """
        print(message)  # noqa: T201

    def display_statistics(self, engine: CardEngine) -> None:
        """Displays the statistics for the user.

        Args:
            engine (CardEngine): The engine relevant to the session.
        """
        statistics = engine.get_statistics()
        self.notify("\n".join(f"{key}: {val}" for key, val in statistics.items()))

    def get_user_feedback(self, feedback: Feedback) -> Feedback:
        """Dynamically prompts for feedback based on Feedback structure."""
        match feedback:
            case BinaryFeedback():
                field_name = feedback.field_name
                while True:
                    try:
                        value = input(f"{field_name}? (y/n): ").strip().lower()
                        if value not in ["y", "yes", "true", "n", "no", "false"]:
                            raise ValueError
                    except ValueError:
                        print("Invalid choice. Please try again.")  # noqa: T201

                    else:
                        feedback.data[field_name] = value in ["y", "yes", "true"]
                        break

            case SingleSelectBooleanFeedback():
                num_options = len(feedback.options)
                print("Choose one of the following options:")  # noqa: T201
                for idx, option in enumerate(feedback.options, 1):
                    print(f"{idx}: {option}")  # noqa: T201

                while True:
                    try:
                        choice = int(
                            input(
                                "Enter the number corresponding to your choice: "
                            ).strip()
                        )
                        if 1 <= choice <= num_options:
                            selected_option = feedback.options[choice - 1]
                            feedback.data = {
                                option: option == selected_option
                                for option in feedback.options
                            }
                        else:
                            raise ValueError
                    except (ValueError, IndexError):
                        print("Invalid choice. Please try again.")  # noqa: T201
                    else:
                        break

            case _:
                msg = f"CLI does not support rendering feedback of type {type(feedback).__name__}."
                raise NotImplementedError(msg)

        feedback.validate()
        return feedback

    def run_session(self, engine: CardEngine) -> None:
        """Runs the session.

        Args:
            engine (CardEngine): The engine relevant to starting the session.
        """
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
                if engine.load_cards(new_file_path, engine.session.strategy):
                    self.notify(f"Successfully loaded new cards from {new_file_path}")
                else:
                    self.notify(f"Failed to load new cards from {new_file_path}")
                continue

            self.display_card_back(card)

            feedback = engine.get_feedback()
            user_feedback = self.get_user_feedback(feedback)
            engine.process_feedback(card, user_feedback)

        # Add a line to separate the summary statistics.
        self.notify("-" * 69)
        self.display_statistics(engine)

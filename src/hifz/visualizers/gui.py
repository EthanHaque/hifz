"""This represents the application graphical user interface."""

import sys

from PyQt6.QtCore import Qt  # type: ignore[import-not-found]
from PyQt6.QtWidgets import (  # type: ignore[import-not-found]
    QApplication,
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from hifz.card_engine import CardEngine
from hifz.models import Card, Feedback, SingleSelectBooleanFeedback, BinaryFeedback
from hifz.visualizers import CardInterface


class GUICardInterface(CardInterface):
    """This class maintains the GUI."""

    def __init__(self) -> None:
        """Instantiates the GUI."""
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle("Flashcard App")
        self.window.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout()

        self.card_label = QLabel("")
        self.card_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_label.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(self.card_label)

        self.flip_button = QPushButton("Flip")
        self.flip_button.clicked.connect(self.flip_card)
        self.layout.addWidget(self.flip_button)

        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.reload_cards)
        self.layout.addWidget(self.reload_button)

        self.window.setLayout(self.layout)

        self.engine: CardEngine
        self.current_card: Card
        self.is_front = True

    def render_feedback(self, feedback: Feedback) -> None:
        """Renders feedback UI dynamically based on feedback structure."""
        self.clear_buttons()
        self.create_feedback_buttons(feedback)

    def clear_buttons(self) -> None:
        """Clears all buttons except the static card label."""
        while self.layout.count() > 1:  # Keep only the card label
            widget = self.layout.takeAt(1).widget()
            if widget:
                widget.deleteLater()

    def create_feedback_buttons(self, feedback: Feedback) -> None:
        """Creates and adds buttons dynamically based on feedback type."""
        match feedback:
            case BinaryFeedback():
                self.add_binary_feedback_buttons(feedback)
            case SingleSelectBooleanFeedback():
                self.add_multi_select_feedback_buttons(feedback)
            case _:
                msg = f"GUI does not support rendering feedback of type {type(feedback).__name__}."
                raise NotImplementedError(msg)

        self.add_navigation_buttons()

    def add_binary_feedback_buttons(self, feedback: BinaryFeedback) -> None:
        """Adds buttons for binary feedback options."""
        field_name = feedback.field_name

        yes_button = QPushButton(f"✅ {field_name}")
        yes_button.clicked.connect(
            lambda: self.submit_feedback(feedback, {field_name: True})
        )
        self.layout.addWidget(yes_button)

        no_button = QPushButton(f"❎ {field_name}")
        no_button.clicked.connect(
            lambda: self.submit_feedback(feedback, {field_name: False})
        )
        self.layout.addWidget(no_button)

    def add_multi_select_feedback_buttons(
        self, feedback: SingleSelectBooleanFeedback
    ) -> None:
        """Adds buttons for multiple selectable feedback options."""
        for option in feedback.options:
            button = QPushButton(option)
            button.clicked.connect(
                lambda _, opt=option: self.submit_feedback(
                    feedback, {key: key == opt for key in feedback.options}
                )
            )
            self.layout.addWidget(button)

    def add_navigation_buttons(self) -> None:
        """Adds static navigation buttons (e.g., Flip, Reload)."""
        flip_button = QPushButton("Flip")
        flip_button.clicked.connect(self.flip_card)
        self.layout.addWidget(flip_button)

        reload_button = QPushButton("Reload")
        reload_button.clicked.connect(self.reload_cards)
        self.layout.addWidget(reload_button)

    def submit_feedback(self, feedback: Feedback, updated_data: dict) -> None:
        """Submits the user feedback."""
        feedback.data = updated_data
        try:
            feedback.validate()
            self.engine.process_feedback(self.current_card, feedback)
            self.show_next_card()
        except (ValueError, TypeError) as e:
            self.notify(str(e))

    def display_card_front(self, card: Card) -> None:
        """Displays the card front."""
        self.card_label.setText(f"Front: {card.front}")
        self.is_front = True

    def display_card_back(self, card: Card) -> None:
        """Displays the card back."""
        self.card_label.setText(f"Back: {card.back}")
        self.is_front = False

    def notify(self, message: str) -> None:
        """Notifies the user with a message."""
        QMessageBox.information(self.window, "Notification", message)

    def run_session(self, engine: CardEngine) -> None:
        """Launches the session."""
        self.engine = engine
        self.show_next_card()
        self.window.show()
        sys.exit(self.app.exec())

    def show_next_card(self) -> None:
        """Displays the next card."""
        self.current_card = self.engine.get_next_card()
        self.display_card_front(self.current_card)
        feedback = self.engine.get_feedback()
        self.render_feedback(feedback)

    def flip_card(self) -> None:
        """Flips the card."""
        if self.is_front:
            self.display_card_back(self.current_card)
        else:
            self.display_card_front(self.current_card)

    def reload_cards(self):
        """Reloads the cards."""
        new_file_path = QFileDialog.getOpenFileName(
            self.window, "Open File", "{$HOME}"
        )[0]
        if self.engine.reload_cards(new_file_path):
            self.notify("Cards reloaded successfully.")
        else:
            self.notify("Failed to reload cards.")
        self.show_next_card()

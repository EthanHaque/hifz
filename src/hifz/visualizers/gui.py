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
from hifz.models import Card
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

        self.correct_button = QPushButton("Correct")
        self.correct_button.clicked.connect(lambda: self.record_result(True))
        self.layout.addWidget(self.correct_button)

        self.incorrect_button = QPushButton("Incorrect")
        self.incorrect_button.clicked.connect(lambda: self.record_result(False))
        self.layout.addWidget(self.incorrect_button)

    def record_result(self, correct: bool) -> None:
        """Records the results."""
        self.engine.process_feedback(self.current_card, correct=correct)
        self.show_next_card()

    def display_card_front(self, card: Card) -> None:
        """Displays the card front."""
        self.card_label.setText(f"Front: {card.front}")
        self.is_front = True

    def display_card_back(self, card: Card) -> None:
        """Displays the card back."""
        self.card_label.setText(f"Front: {card.front}")
        self.card_label.setText(f"Back: {card.back}")
        self.is_front = False

    def notify(self, message: str) -> None:
        """Notifies the user with message."""
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

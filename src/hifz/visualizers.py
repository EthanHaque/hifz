import sys
from abc import ABC, abstractmethod

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from hifz.card_engine import CardEngine
from hifz.models import Card


class CardInterface(ABC):
    @abstractmethod
    def display_card_front(self, card: Card) -> None:
        pass

    @abstractmethod
    def display_card_back(self, card: Card) -> None:
        pass

    @abstractmethod
    def notify(self, message: str) -> None:
        pass

    @abstractmethod
    def run_session(self, engine: "CardEngine") -> None:
        """Controls the flow of the session, interacting with the engine as needed."""


class CLICardInterface(CardInterface):
    def display_card_front(self, card: Card) -> None:
        print(f"\nFront: {card.front}")  # noqa: T201

    def display_card_back(self, card: Card) -> None:
        print(f"Back: {card.back}")  # noqa: T201

    def notify(self, message: str) -> None:
        print(message)  # noqa: T201

    def run_session(self, engine: CardEngine) -> None:
        self.notify(
            "Starting flashcard session... Type 'q' to quit, 'reload' to load new cards."
        )

        while True:
            card = engine.get_next_card()
            self.display_card_front(card)

            action = (
                input(
                    "(Press Enter to see the back, 'q' to quit, or 'reload' to switch cards): "
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


class GUICardInterface(CardInterface):
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle("Flashcard App")
        self.window.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout()

        self.card_label = QLabel("")
        self.card_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_label.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(self.card_label)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next_card)
        self.layout.addWidget(self.next_button)

        self.flip_button = QPushButton("Flip")
        self.flip_button.clicked.connect(self.flip_card)
        self.layout.addWidget(self.flip_button)

        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.reload_cards)
        self.layout.addWidget(self.reload_button)

        self.window.setLayout(self.layout)

        self.engine = None
        self.current_card = None
        self.is_front = True

    def display_card_front(self, card: Card) -> None:
        self.card_label.setText(f"Front: {card.front}")
        self.is_front = True

    def display_card_back(self, card: Card) -> None:
        self.card_label.setText(f"Back: {card.back}")
        self.is_front = False

    def notify(self, message: str) -> None:
        QMessageBox.information(self.window, "Notification", message)

    def run_session(self, engine: CardEngine) -> None:
        self.engine = engine
        self.show_next_card()
        self.window.show()
        sys.exit(self.app.exec())

    def show_next_card(self):
        if self.engine:
            self.current_card = self.engine.get_next_card()
            self.display_card_front(self.current_card)

    def flip_card(self):
        if self.current_card:
            if self.is_front:
                self.display_card_back(self.current_card)
            else:
                self.display_card_front(self.current_card)

    def reload_cards(self):
        new_file_path, ok = QInputDialog.getText(
            self.window, "Reload Cards", "Enter new file path:"
        )
        if ok and new_file_path:
            if self.engine.reload_cards(new_file_path):
                self.notify("Cards reloaded successfully.")
            else:
                self.notify("Failed to reload cards.")

from unittest.mock import patch

from hifz.models import Card
from hifz.visualizers import TUICardInterface


def test_tui_display_card_front():
    interface = TUICardInterface()
    card = Card("Hello", "World")

    with patch("builtins.print") as mocked_print:
        interface.display_card_front(card)
        mocked_print.assert_called_once_with("\nFront: Hello")


def test_tui_display_card_back():
    interface = TUICardInterface()
    card = Card("Hello", "World")

    with patch("builtins.print") as mocked_print:
        interface.display_card_back(card)
        mocked_print.assert_called_once_with("Back: World")


def test_tui_get_user_input():
    interface = TUICardInterface()

    with patch("builtins.input", return_value="test_input"):
        assert interface.get_user_input("Prompt: ") == "test_input"

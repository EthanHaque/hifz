from hifz.models import Card
from hifz.visualizers.cli import CLICardInterface


def test_cli_display_card_front(mocker):
    interface = CLICardInterface()
    card = Card("Hello", "World")

    mocked_print = mocker.patch("builtins.print")
    interface.display_card_front(card)
    mocked_print.assert_called_once_with("\nFront: Hello")


def test_cli_display_card_back(mocker):
    interface = CLICardInterface()
    card = Card("Hello", "World")

    mocked_print = mocker.patch("builtins.print")
    interface.display_card_back(card)
    mocked_print.assert_called_once_with("Back: World")

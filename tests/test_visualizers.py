from hifz.models import Card
from hifz.visualizers.cli import CLIVisualizer


def test_cli_display_card_front(mocker):
    """Test display of card front in the CLI.

    Verifies that the `display_card_front` method in CLICardInterface
    correctly outputs the card's front text to the console.

    Args:
        mocker (MockerFixture): Fixture for mocking dependencies.

    Asserts:
        - `print` is called once with the correct text for the card's front.
    """
    visualizer = CLIVisualizer()
    card = Card("Hello", "World")

    mocked_print = mocker.patch("builtins.print")
    visualizer.display_card_front(card)
    mocked_print.assert_called_once_with("\nFront: Hello")


def test_cli_display_card_back(mocker):
    """Test display of card back in the CLI.

    Verifies that the `display_card_back` method in CLICardInterface
    correctly outputs the card's back text to the console.

    Args:
        mocker (MockerFixture): Fixture for mocking dependencies.

    Asserts:
        - `print` is called once with the correct text for the card's back.
    """
    visualizer = CLIVisualizer()
    card = Card("Hello", "World")

    mocked_print = mocker.patch("builtins.print")
    visualizer.display_card_back(card)
    mocked_print.assert_called_once_with("Back: World")

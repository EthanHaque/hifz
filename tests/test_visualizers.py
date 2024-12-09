from hifz.models import BinaryFeedback, Card
from hifz.visualizers.cli import CLICardInterface


def test_cli_display_card_front(mocker):
    """Test display of card front in the CLI.

    Verifies that the `display_card_front` method in CLICardInterface
    correctly outputs the card's front text to the console.

    Args:
        mocker (MockerFixture): Fixture for mocking dependencies.

    Asserts:
        - `print` is called once with the correct text for the card's front.
    """
    interface = CLICardInterface()
    card = Card("Hello", "World")

    mocked_print = mocker.patch("builtins.print")
    interface.display_card_front(card)
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
    interface = CLICardInterface()
    card = Card("Hello", "World")

    mocked_print = mocker.patch("builtins.print")
    interface.display_card_back(card)
    mocked_print.assert_called_once_with("Back: World")


def test_cli_invalid_feedback(mocker):
    """Tests that when the CLI prompts for y/n and something else is inputted
    that the CLI asks the user to try again."""
    interface = CLICardInterface()
    feedback = BinaryFeedback("Correct")

    # Two invalid inputs then a valid input.
    mocked_input = mocker.patch("builtins.input", side_effect=["u", "u", "y"])
    mocked_print = mocker.patch("builtins.print")

    interface.get_user_feedback(feedback)

    # Asks for three inputs and prints the error message after the first two.
    assert mocked_input.call_count == 3
    assert mocked_print.call_count == 2
    mocked_print.assert_any_call("Invalid choice. Please try again.")

import pytest

from hifz.models import (
    BinaryFeedback,
    SingleSelectBooleanFeedback,
    Card,
)


def test_binary_feedback_initialization():
    """Test BinaryFeedback initializes correctly with a single field."""
    feedback = BinaryFeedback("correct")
    assert feedback.data == {
        "correct": False
    }, f"{feedback.__class__.__name__} did not initialize correctly."


def test_binary_feedback_validation_passes():
    """Test BinaryFeedback validation passes for correct input."""
    feedback = BinaryFeedback("correct")
    feedback.data["correct"] = True
    feedback.validate()


def test_binary_feedback_validation_fails():
    """Test BinaryFeedback validation fails for multiple True values."""
    feedback = BinaryFeedback("correct")
    feedback.data["correct"] = True
    feedback.data["extra"] = True  # Adding an invalid field to simulate failure
    with pytest.raises(
        ValueError, match=f"{feedback.__class__.__name__} can only have one value"
    ):
        feedback.validate()


def test_binary_feedback_metadata():
    """Test BinaryFeedback metadata generation."""
    feedback = BinaryFeedback("correct")
    metadata = feedback.get_metadata()
    assert metadata == {
        "correct": {"type": bool}
    }, f"{feedback.__class__.__name__} metadata is incorrect."


def test_single_select_boolean_feedback_initialization():
    """Test SingleSelectBooleanFeedback initializes correctly with multiple options."""
    feedback = SingleSelectBooleanFeedback("easy", "medium", "hard")
    assert feedback.data == {
        "easy": False,
        "medium": False,
        "hard": False,
    }, f"{feedback.__class__.__name__} did not initialize correctly."


def test_single_select_boolean_feedback_validation_passes():
    """Test SingleSelectBooleanFeedback validation passes for exactly one True value."""
    feedback = SingleSelectBooleanFeedback("easy", "medium", "hard")
    feedback.data["medium"] = True
    feedback.validate()


def test_single_select_boolean_feedback_validation_fails_no_true():
    """Test SingleSelectBooleanFeedback validation fails when no options are True."""
    feedback = SingleSelectBooleanFeedback("easy", "medium", "hard")
    with pytest.raises(
        ValueError,
        match=f"Exactly one field must be True in {feedback.__class__.__name__}",
    ):
        feedback.validate()


def test_single_select_boolean_feedback_validation_fails_multiple_true():
    """Test SingleSelectBooleanFeedback validation fails when multiple options are True."""
    feedback = SingleSelectBooleanFeedback("easy", "medium", "hard")
    feedback.data["easy"] = True
    feedback.data["medium"] = True
    with pytest.raises(
        ValueError,
        match=f"Exactly one field must be True in {feedback.__class__.__name__}",
    ):
        feedback.validate()


def test_single_select_boolean_feedback_metadata():
    """Test SingleSelectBooleanFeedback metadata generation."""
    feedback = SingleSelectBooleanFeedback("easy", "medium", "hard")
    metadata = feedback.get_metadata()
    assert metadata == {
        "easy": {"type": bool},
        "medium": {"type": bool},
        "hard": {"type": bool},
    }, f"{feedback.__class__.__name__} metadata is incorrect."


def test_feedback_summary_aggregation():
    """Test that FeedbackSummary correctly aggregates feedback."""
    card = Card(front="Test Front", back="Test Back")

    card.statistics.update("correct", 1, lambda existing, new: (existing or 0) + new)
    card.statistics.update("correct", 1, lambda existing, new: (existing or 0) + new)
    card.statistics.update("incorrect", 1, lambda existing, new: (existing or 0) + new)
    card.statistics.update("incorrect", 1, lambda existing, new: (existing or 0) + new)

    assert (
        card.statistics.get("correct") == 2
    ), "FeedbackSummary did not aggregate 'correct' values correctly."
    assert (
        card.statistics.get("incorrect") == 2
    ), "FeedbackSummary did not aggregate 'incorrect' values correctly."


def test_feedback_summary_with_binary_feedback():
    """Test FeedbackSummary updates correctly with BinaryFeedback."""
    card = Card(front="Test Front", back="Test Back")
    feedback = BinaryFeedback("correct")

    feedback.data["correct"] = True
    card.statistics.update(
        "correct",
        1 if feedback.get("correct") else 0,
        lambda existing, new: (existing or 0) + new,
    )

    feedback.data["correct"] = False
    card.statistics.update(
        "incorrect",
        1 if not feedback.get("correct") else 0,
        lambda existing, new: (existing or 0) + new,
    )

    assert (
        card.statistics.get("correct") == 1
    ), "FeedbackSummary did not aggregate 'correct' feedback correctly."
    assert (
        card.statistics.get("incorrect") == 1
    ), "FeedbackSummary did not aggregate 'incorrect' feedback correctly."

"""This represents the application entrypoint."""

import argparse
from pathlib import Path

from hifz.card_engine import CardEngine
from hifz.learning_strategies import (
    STRATEGY_NAME_TO_CLASS,
    CardStrategy,
)
from hifz.visualizers import Visualizer
from hifz.visualizers.cli import CLIVisualizer


def get_args() -> argparse.Namespace:
    """Returns the parsed arguments."""
    parser = argparse.ArgumentParser(description="A flashcard memorization program.")

    parser.add_argument(
        "visualizer",
        choices=["cli", "gui", "tui"],
        help="The type of visualizer to use.",
    )
    parser.add_argument(
        "strategy",
        choices=list(STRATEGY_NAME_TO_CLASS.keys()),
        help=f"The card memorization strategy to use. Options: {', '.join(STRATEGY_NAME_TO_CLASS.keys())}.",
    )
    parser.add_argument(
        "--save",
        type=Path,
        help="Optional: Path to save progress after the session ends.",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Optional: Path to save progress after the session ends.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--source",
        type=str,
        help="The source of the desired card collection, either a URL or a file path (e.g., .csv or .json).",
    )
    group.add_argument(
        "--resume",
        type=str,
        help="Path to a saved session file to resume progress.",
    )

    return parser.parse_args()


def get_strategy(strategy_name: str) -> CardStrategy:
    """Returns the desired strategy."""
    strategy_cls = STRATEGY_NAME_TO_CLASS.get(strategy_name)
    if not strategy_cls:
        error_message = f"{strategy_name} is not a valid strategy. Supported strategies: {', '.join(STRATEGY_NAME_TO_CLASS.keys())}."
        raise ValueError(error_message)
    return strategy_cls()


def get_visualizer(visualizer: str) -> Visualizer:
    """Returns the desired visualizer."""
    match visualizer:
        case "cli":
            return CLIVisualizer()
        case "gui":
            try:
                from hifz.visualizers.gui import GUIVisualizer
            except ImportError as e:
                raise e
            return GUIVisualizer()
        case "tui":
            try:
                from hifz.visualizers.tui import TUIVisualizer
            except ImportError as e:
                raise e
            return TUIVisualizer()
        case _:
            error_message = f"{visualizer} is not a valid visualizer"
            raise ValueError(error_message)


def main() -> None:
    """The project entrypoint."""
    args = get_args()

    strategy = get_strategy(args.strategy)
    visualizer = get_visualizer(args.visualizer)

    engine = CardEngine(strategy)
    if args.resume:
        engine.load_progress(args.resume)
    else:
        engine.load_cards(args.source, args.reverse)

    visualizer.run_session(engine)

    if args.save:
        engine.save_progress(args.save)


if __name__ == "__main__":
    main()

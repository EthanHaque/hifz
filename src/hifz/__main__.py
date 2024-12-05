"""This represents the application entrypoint."""

import argparse

from hifz.card_engine import CardEngine
from hifz.learning_strategies import (
    CardStrategy,
    MasteryStrategy,
    RandomStrategy,
    SequentialStrategy,
)
from hifz.visualizers import CardInterface
from hifz.visualizers.cli import CLICardInterface


def get_args() -> argparse.Namespace:
    """Returns the parsed arguments."""
    parser = argparse.ArgumentParser(description="A flashcard memorization program.")
    parser.add_argument("visualizer", help="The type of visualizer to use.")
    parser.add_argument("file_path", help="The file path of desired card collection.")
    parser.add_argument("strategy", help="The card memorization strategy to use.")
    return parser.parse_args()


def get_strategy(strategy: str) -> CardStrategy:
    """Returns the desired strategy."""
    match strategy:
        case "random":
            return RandomStrategy()
        case "sequential":
            return SequentialStrategy()
        case "mastery":
            return MasteryStrategy()
        case _:
            error_message = f"{strategy} is not a valid strategy"
            raise ValueError(error_message)


def get_visualizer(visualizer: str) -> CardInterface:
    """Returns the desired visualizer."""
    match visualizer:
        case "cli":
            return CLICardInterface()
        case "gui":
            try:
                from hifz.visualizers.gui import GUICardInterface
            except ImportError as e:
                raise e
            return GUICardInterface()
        case _:
            error_message = f"{visualizer} is not a valid visualizer"
            raise ValueError(error_message)


def main() -> None:
    """The project entrypoint."""
    args = get_args()

    strategy = get_strategy(args.strategy)
    interface = get_visualizer(args.visualizer)

    engine = CardEngine(strategy)
    engine.load_cards(args.file_path)

    interface.run_session(engine)


if __name__ == "__main__":
    main()

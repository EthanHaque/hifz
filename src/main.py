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
from hifz.visualizers.tui import TUICardInterface


def parse_args() -> argparse.Namespace:
    """Returns the parsed arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("visualizer", help="Type of visualizer to use.")
    parser.add_argument("filepath", help="Path to card file")
    parser.add_argument("strategy", help="Learning strategy")
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
        case "tui":
            return TUICardInterface()
        case _:
            error_message = f"{visualizer} is not a valid visualizer"
            raise ValueError(error_message)


def main() -> None:
    """The project entrypoint."""
    args = parse_args()

    strategy = get_strategy(args.strategy)
    interface = get_visualizer(args.visualizer)

    engine = CardEngine(strategy)
    engine.load_cards(args.filepath)

    interface.run_session(engine)


if __name__ == "__main__":
    main()

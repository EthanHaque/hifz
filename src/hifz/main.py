import argparse

from hifz.card_engine import CardEngine
from hifz.learning_strategies import CardStrategy, RandomStrategy, SequentialStrategy
from hifz.visualizers import CLICardInterface


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="Path to card file")
    parser.add_argument("strategy", help="Learning strategy")
    return parser.parse_args()


def get_strategy(strategy: str) -> CardStrategy:
    match strategy:
        case "random":
            return RandomStrategy()
        case "sequential":
            return SequentialStrategy()
        case _:
            error_message = f"{strategy} is not a valid strategy"
            raise ValueError(error_message)


def main():
    args = parse_args()

    strategy = get_strategy(args.strategy)
    interface = CLICardInterface()

    engine = CardEngine(strategy)
    engine.load_cards(args.filepath)

    interface.run_session(engine)


if __name__ == "__main__":
    main()

import argparse

from hifz.card_engine import CardEngine
from hifz.dataserver import DataServer
from hifz.learning_strategies import CardStrategy, RandomStrategy, SequentialStrategy
from hifz.models import Card
from hifz.visualizers import TUICardInterface


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="Path to card file")
    parser.add_argument("strategy", help="Learning strategy")
    return parser.parse_args()


def load_cards(file_path: str) -> list[Card]:
    data_server = DataServer()

    try:
        return data_server.read_entries(file_path)
    except Exception as _:
        return []


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

    cards = load_cards(args.filepath)
    strategy = get_strategy(args.strategy)
    interface = TUICardInterface()

    engine = CardEngine(cards, strategy, interface)

    engine.run()


if __name__ == "__main__":
    main()

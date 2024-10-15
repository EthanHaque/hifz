from hifz.dataserver import DataServer
from hifz.learning_strategies import RandomStrategy, SequentialStrategy
from hifz.card_engine import CardEngine
from hifz.visualizers import TUICardInterface


def load_cards():
    data_server = DataServer()
    file_path = input("Enter the path to your card file (CSV/JSON): ").strip()

    try:
        cards = data_server.read_entries(file_path)
        print(f"Loaded {len(cards)} cards.") # noqa: T201
        return cards
    except Exception as e:
        print(f"Error: {e}") # noqa: T201
        return []


def choose_strategy():
    print("\nChoose a learning strategy:") # noqa: T201
    print("1. Random") # noqa: T201
    print("2. Sequential") # noqa: T201
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        return RandomStrategy()
    elif choice == "2":
        return SequentialStrategy()
    else:
        print("Invalid choice, defaulting to Sequential.") # noqa: T201
        return SequentialStrategy()


def main():
    print("Welcome to hifz") # noqa: T201

    cards = load_cards()
    if not cards:
        print("No cards loaded. Exiting...") # noqa: T201
        return

    strategy = choose_strategy()

    interface = TUICardInterface()

    engine = CardEngine(cards, strategy, interface)
    engine.run()


if __name__ == "__main__":
    main()

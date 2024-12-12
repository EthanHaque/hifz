"""This module maintains the utility models and methods for the program."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from hifz.learning_strategies import (
    STRATEGY_NAME_TO_CLASS,
    CardStrategy,
)
from hifz.models import Card


class CardSession:
    """This class maintains the logic associated with starting a Card Session."""

    def __init__(self, cards: list[Card], strategy: CardStrategy) -> None:
        """Instantiates the CardSession."""
        self.cards = cards
        self.strategy = strategy

    def next_card(self) -> Card:
        """Returns the next card."""
        return self.strategy.get_next_card(self.cards)

    def save_progress(self, file_path: Path) -> None:
        """Saves the session state to a file."""
        data = {
            "metadata": {
                "version": "1.0",
                "timestamp": datetime.now().isoformat(),
            },
            "session": {
                "strategy": {
                    **self.strategy.to_dict(),
                },
                "cards": [card.to_dict() for card in self.cards],
            },
        }
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, cls=SessionEncoder)

    @classmethod
    def load_progress(cls, file_path: Path) -> "CardSession":
        """Loads the session state from a file."""
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        metadata = data.get("metadata", {})
        if metadata.get("version") != "1.0":
            msg = "Unsupported session version."
            raise ValueError(msg)

        session_data = data["session"]
        strategy_info = session_data["strategy"]
        strategy_name = strategy_info["type"]
        if strategy_name not in STRATEGY_NAME_TO_CLASS:
            msg = f"Unsupported strategy type: {strategy_name}"
            raise ValueError(msg)
        strategy_class = STRATEGY_NAME_TO_CLASS[strategy_name]
        strategy = strategy_class.from_dict(strategy_info)

        cards = [Card.from_dict(card_data) for card_data in session_data["cards"]]
        return cls(cards=cards, strategy=strategy)

    def aggregate_statistics(self) -> dict[str, Any]:
        """Gets global statistics from the Strategy."""
        return self.strategy.aggregate_statistics(self.cards)

    def __repr__(self) -> str:
        """Machine-readable representation of the CardSession."""
        return (
            f"{self.__class__.__name__}(cards=[{', '.join(repr(card) for card in self.cards)}], "
            f"strategy={self.strategy!r})"
        )

    def __str__(self) -> str:
        """User-friendly string representation of the CardSession."""
        card_details = "\n".join(
            f"  - Front: {card.front}, Back: {card.back}, Statistics: {card.statistics.data}"
            for card in self.cards
        )
        strategy_details = json.dumps(self.strategy.to_dict(), indent=4)
        return (
            f"{self.__class__.__name__}:\n"
            f"Strategy:\n{strategy_details}\n\n"
            f"Cards:\n{card_details}"
        )


class SessionEncoder(json.JSONEncoder):
    """This class helps encode non-serializable data."""

    def default(self, o):
        """Convert non-serializable objects to a serializable format."""
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


class SessionDecoder(json.JSONDecoder):
    """This class helps decode serialized data back into their original objects."""

    def __init__(self, *args, **kargs) -> None:
        """Initalizes the object."""
        super().__init__(object_hook=self.obj_hook, *args, **kargs)  # noqa: B026

    def obj_hook(self, obj):
        """Convert serialized objects back into their original format."""
        if "timestamp" in obj:
            obj["timestamp"] = datetime.fromisoformat(obj["timestamp"])
        if "cards" in obj:
            for card in obj["cards"]:
                if "due" in card:
                    card["due"] = datetime.fromisoformat(card["due"])
        return obj

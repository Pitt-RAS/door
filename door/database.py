"""Card database."""

import logging
from pathlib import Path
from dataclasses import dataclass
from threading import RLock
from typing import Dict, Optional

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@dataclass
class CardEntry:
    """A single card."""

    name: str
    card: str


class CardDatabase:
    """Card database."""

    def __init__(self, file: Path = Path("/app/door/door/database.txt")) -> None:
        """Construct a card database."""
        self.file = file
        self.entries: Dict[str, CardEntry] = {}
        self.lock = RLock()

    def load(self) -> None:
        """Load the database, ignoring local changes."""
        with self.lock:
            self.entries = {}
            if not self.file.exists():
                log.debug("Created new database")
                self.file.touch()
            with self.file.open("r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entry = line.strip().split(",")
                        self.add(CardEntry(*entry))
                log.info("Loaded %d cards", len(self.entries))

    def add(self, card: CardEntry) -> None:
        """Add a card entry."""
        with self.lock:
            self.entries[card.card] = card

    def commit(self) -> None:
        """Commit database changes to the file."""
        with self.lock:
            with self.file.open("w") as f:
                for entry in self.entries.values():
                    f.write(f"{entry.name},{entry.card}\n")

    def get(self, card: str) -> Optional[CardEntry]:
        """Get a card entry if it exists in the database."""
        with self.lock:
            return self.entries.get(card)


database = CardDatabase()

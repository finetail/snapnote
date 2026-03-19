"""Persistent JSON-based note storage."""

from __future__ import annotations

import json
from pathlib import Path

from platformdirs import user_data_dir

from snapnote.models import Note

_DATA_DIR = Path(user_data_dir("snapnote", "snapnote"))
_NOTES_FILE = _DATA_DIR / "notes.json"


class NoteStore:
    def __init__(self, path: Path = _NOTES_FILE) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> list[Note]:
        if not self._path.exists():
            return []
        with self._path.open() as f:
            return [Note.from_dict(d) for d in json.load(f)]

    def _dump(self, notes: list[Note]) -> None:
        with self._path.open("w") as f:
            json.dump([n.to_dict() for n in notes], f, indent=2)

    def save(self, note: Note) -> None:
        notes = self._load()
        notes.append(note)
        self._dump(notes)

    def list_notes(self, tag: str | None = None, limit: int = 20) -> list[Note]:
        notes = self._load()
        if tag:
            notes = [n for n in notes if tag in n.tags]
        return sorted(notes, key=lambda n: n.created_at, reverse=True)[:limit]

    def search(self, query: str) -> list[Note]:
        return [n for n in self._load() if query.lower() in n.body.lower()]

    def delete(self, id_prefix: str) -> bool:
        notes = self._load()
        filtered = [n for n in notes if not n.id.startswith(id_prefix)]
        if len(filtered) == len(notes):
            return False
        self._dump(filtered)
        return True

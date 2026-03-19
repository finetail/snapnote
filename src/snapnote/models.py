"""Data models for snapnote."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Note:
    id: str
    body: str
    tags: list[str]
    created_at: datetime

    @classmethod
    def new(cls, body: str, tags: list[str] | None = None) -> "Note":
        return cls(
            id=str(uuid.uuid4()),
            body=body,
            tags=tags or [],
            created_at=datetime.now(tz=timezone.utc),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "body": self.body,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        return cls(
            id=data["id"],
            body=data["body"],
            tags=data.get("tags", []),
            created_at=datetime.fromisoformat(data["created_at"]),
        )

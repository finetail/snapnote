"""Tests for the Note model."""

from snapnote.models import Note


def test_new_note_has_id_and_timestamp():
    note = Note.new("hello world")
    assert note.id
    assert note.body == "hello world"
    assert note.tags == []
    assert note.created_at is not None


def test_new_note_with_tags():
    note = Note.new("tagged note", tags=["work", "urgent"])
    assert "work" in note.tags
    assert "urgent" in note.tags


def test_round_trip_serialization():
    original = Note.new("round trip test", tags=["test"])
    restored = Note.from_dict(original.to_dict())
    assert restored.id == original.id
    assert restored.body == original.body
    assert restored.tags == original.tags
    assert restored.created_at == original.created_at

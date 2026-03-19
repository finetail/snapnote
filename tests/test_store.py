"""Tests for NoteStore."""

import pytest
from pathlib import Path

from snapnote.store import NoteStore
from snapnote.models import Note


@pytest.fixture
def store(tmp_path: Path) -> NoteStore:
    return NoteStore(path=tmp_path / "notes.json")


def test_save_and_list(store: NoteStore):
    note = Note.new("first note")
    store.save(note)
    results = store.list_notes()
    assert len(results) == 1
    assert results[0].body == "first note"


def test_filter_by_tag(store: NoteStore):
    store.save(Note.new("work note", tags=["work"]))
    store.save(Note.new("personal note", tags=["personal"]))
    work = store.list_notes(tag="work")
    assert len(work) == 1
    assert work[0].body == "work note"


def test_search(store: NoteStore):
    store.save(Note.new("buy groceries"))
    store.save(Note.new("call dentist"))
    results = store.search("groceries")
    assert len(results) == 1


def test_delete(store: NoteStore):
    note = Note.new("to be deleted")
    store.save(note)
    removed = store.delete(note.id[:8])
    assert removed is True
    assert store.list_notes() == []


def test_delete_nonexistent(store: NoteStore):
    assert store.delete("deadbeef") is False

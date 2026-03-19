"""Tests for the snapnote CLI using Click's CliRunner."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from snapnote.cli import main
from snapnote.store import NoteStore


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def store_path(tmp_path: Path) -> Path:
    return tmp_path / "notes.json"


def test_add_note(runner: CliRunner, store_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """snapnote add Hello saves a note."""
    monkeypatch.setattr("snapnote.cli.NoteStore", lambda: NoteStore(path=store_path))
    result = runner.invoke(main, ["add", "Hello"])
    assert result.exit_code == 0
    assert "Saved" in result.output
    store = NoteStore(path=store_path)
    notes = store.list_notes()
    assert len(notes) == 1
    assert notes[0].body == "Hello"


def test_add_note_with_tags(runner: CliRunner, store_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """snapnote add with -t flag saves a tagged note."""
    monkeypatch.setattr("snapnote.cli.NoteStore", lambda: NoteStore(path=store_path))
    result = runner.invoke(main, ["add", "Tagged memo", "-t", "work", "-t", "urgent"])
    assert result.exit_code == 0
    assert "Saved" in result.output
    store = NoteStore(path=store_path)
    notes = store.list_notes()
    assert len(notes) == 1
    assert "work" in notes[0].tags
    assert "urgent" in notes[0].tags


def test_list_notes(runner: CliRunner, store_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """snapnote list shows added notes."""
    monkeypatch.setattr("snapnote.cli.NoteStore", lambda: NoteStore(path=store_path))
    runner.invoke(main, ["add", "My list note"])
    result = runner.invoke(main, ["list"])
    assert result.exit_code == 0
    assert "My list note" in result.output


def test_search_notes(runner: CliRunner, store_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """snapnote search returns matching notes."""
    monkeypatch.setattr("snapnote.cli.NoteStore", lambda: NoteStore(path=store_path))
    runner.invoke(main, ["add", "buy groceries today"])
    runner.invoke(main, ["add", "call dentist"])
    result = runner.invoke(main, ["search", "groceries"])
    assert result.exit_code == 0
    assert "groceries" in result.output


def test_delete_note(runner: CliRunner, store_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """snapnote delete removes the note by ID prefix."""
    monkeypatch.setattr("snapnote.cli.NoteStore", lambda: NoteStore(path=store_path))
    runner.invoke(main, ["add", "note to delete"])
    store = NoteStore(path=store_path)
    notes = store.list_notes()
    assert len(notes) == 1
    note_id_prefix = notes[0].id[:8]
    result = runner.invoke(main, ["delete", note_id_prefix], input="y\n")
    assert result.exit_code == 0
    assert "Deleted" in result.output
    remaining = store.list_notes()
    assert remaining == []

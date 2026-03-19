"""Entry point for the snapnote CLI."""

import click
from rich.console import Console

from snapnote.store import NoteStore
from snapnote.models import Note

console = Console()


@click.group()
@click.version_option()
def main() -> None:
    """snapnote — jot, find, and manage plaintext notes."""


@main.command("add")
@click.argument("text", nargs=-1, required=True)
@click.option("-t", "--tag", multiple=True, help="Tag the note (repeatable).")
def add_note(text: tuple[str, ...], tag: tuple[str, ...]) -> None:
    """Add a new note."""
    body = " ".join(text)
    note = Note.new(body, tags=list(tag))
    store = NoteStore()
    store.save(note)
    console.print(f"[green]Saved[/green] note [bold]{note.id[:8]}[/bold]")


@main.command("list")
@click.option("-t", "--tag", default=None, help="Filter by tag.")
@click.option("-n", "--limit", default=20, show_default=True, help="Max results.")
def list_notes(tag: str | None, limit: int) -> None:
    """List recent notes."""
    store = NoteStore()
    notes = store.list_notes(tag=tag, limit=limit)
    if not notes:
        console.print("[dim]No notes found.[/dim]")
        return
    for n in notes:
        console.print(f"[cyan]{n.id[:8]}[/cyan]  {n.created_at:%Y-%m-%d}  {n.body[:72]}")


@main.command("search")
@click.argument("query")
def search_notes(query: str) -> None:
    """Full-text search across all notes."""
    store = NoteStore()
    results = store.search(query)
    if not results:
        console.print(f"[dim]No results for '{query}'.[/dim]")
        return
    for n in results:
        highlighted = n.body.replace(query, f"[bold yellow]{query}[/bold yellow]")
        console.print(f"[cyan]{n.id[:8]}[/cyan]  {highlighted[:80]}")


@main.command("delete")
@click.argument("note_id")
@click.confirmation_option(prompt="Delete this note?")
def delete_note(note_id: str) -> None:
    """Delete a note by its ID prefix."""
    store = NoteStore()
    removed = store.delete(note_id)
    if removed:
        console.print(f"[red]Deleted[/red] note [bold]{note_id}[/bold]")
    else:
        console.print(f"[yellow]Note '{note_id}' not found.[/yellow]")

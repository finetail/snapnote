# snapnote

A fast CLI tool for capturing and searching plaintext notes — jot ideas, tag them, and find them again in seconds.

[![CI](https://github.com/demo-user/snapnote/actions/workflows/ci.yml/badge.svg)](https://github.com/demo-user/snapnote/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

- **Instant capture** — add a note from the terminal in one command
- **Tagging** — label notes with one or more tags for easy filtering
- **Full-text search** — case-insensitive substring search across all notes
- **Chronological listing** — view recent notes with optional tag filtering and result limits
- **Safe deletion** — delete notes by ID prefix with a confirmation prompt
- **Persistent storage** — notes are stored as JSON in the platform-appropriate user data directory
- **Rich output** — colour-highlighted terminal output via [Rich](https://github.com/Textualize/rich)

---

## Tech Stack

| Layer | Library |
|---|---|
| CLI framework | [Click](https://click.palletsprojects.com/) >= 8.1 |
| Terminal output | [Rich](https://github.com/Textualize/rich) >= 13.0 |
| Data directory | [platformdirs](https://github.com/platformdirs/platformdirs) >= 4.0 |
| Build backend | [setuptools](https://setuptools.pypa.io/) >= 68 |
| Linting | [Ruff](https://docs.astral.sh/ruff/) >= 0.3 |
| Type checking | [mypy](https://mypy-lang.org/) >= 1.8 |
| Testing | [pytest](https://docs.pytest.org/) >= 7.4 + pytest-cov >= 4.1 |

---

## Installation

Install from PyPI:

```bash
pip install snapnote
```

Or clone the repository and install in editable mode with all development dependencies:

```bash
git clone https://github.com/demo-user/snapnote.git
cd snapnote
pip install -e ".[dev]"
```

After installation the `snapnote` command is available on your `PATH`.

---

## Usage

### Add a note

```bash
# Plain text note
snapnote add Buy oat milk and bananas

# Note with one tag
snapnote add Finish the quarterly report -t work

# Note with multiple tags
snapnote add Read "Designing Data-Intensive Applications" -t reading -t tech
```

The `-t` / `--tag` flag is repeatable; pass it multiple times to apply several tags to a single note.

### List notes

```bash
# Show the 20 most recent notes (default)
snapnote list

# Limit output to 5 notes
snapnote list -n 5

# Filter by tag
snapnote list --tag work

# Combine tag filter and limit
snapnote list -t reading -n 10
```

> Note: the list output shows each note's ID prefix, date, and body. Tags are not printed inline but can be used as a filter with `-t`.

### Search notes

```bash
# Full-text search (case-insensitive)
snapnote search groceries

snapnote search "quarterly report"
```

### Delete a note

```bash
# Delete by the first 8 characters of the note ID shown in list/search output
snapnote delete a1b2c3d4
# You will be prompted: "Delete this note? [y/N]"
```

### Global options

```bash
# Display the installed version
snapnote --version

# Show help for any command
snapnote --help
snapnote add --help
snapnote list --help
snapnote search --help
snapnote delete --help
```

---

## Running Tests

```bash
# Run the full test suite with coverage report
pytest

# Run a specific test file
pytest tests/test_store.py

# Run with verbose output
pytest -v
```

Coverage is reported automatically in the terminal. The CI pipeline also runs the linter and type checker:

```bash
ruff check .
mypy src
```

---

## Project Structure

```
snapnote/
├── src/
│   └── snapnote/
│       ├── __init__.py     # Package version declaration (__version__ = "0.1.0")
│       ├── cli.py          # Click command definitions (add, list, search, delete)
│       ├── models.py       # Note dataclass with serialisation helpers
│       └── store.py        # JSON-backed NoteStore (save, list, search, delete)
├── tests/
│   ├── __init__.py
│   ├── test_models.py      # Unit tests for the Note model
│   └── test_store.py       # Integration tests for NoteStore
├── pyproject.toml          # Project metadata, dependencies, tool config
└── README.md
```

---

## Data Storage

Notes are saved as a JSON file in the platform-appropriate user data directory:

| Platform | Path |
|---|---|
| Linux | `~/.local/share/snapnote/notes.json` |
| macOS | `~/Library/Application Support/snapnote/notes.json` |
| Windows | `%LOCALAPPDATA%\snapnote\snapnote\notes.json` |

The directory is created automatically on first use.

---

## Contributing

1. Fork the repository and create a feature branch.
2. Install the dev dependencies: `pip install -e ".[dev]"`
3. Make your changes and add tests under `tests/`.
4. Ensure the full check suite passes before opening a pull request:

```bash
ruff check .
mypy src
pytest
```

---

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).

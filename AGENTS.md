# AGENTS

This file explains the structure of the project and sets rules for Codex when editing files.

## Project layout

- `mistocr/` – main Python package containing CLI and helper modules.
  - `cli.py` – command line interface and option parsing.
  - `api.py` – calls the Mistral OCR API.
  - `config.py` – stores and retrieves API keys.
  - `formatter.py` – converts OCR responses to markdown, plain text or PDF.
- `tests/` – pytest suite covering the CLI helpers and formatters.
- `pyproject.toml` – Python package configuration and dependencies.

## Rules for Codex

- Run `pytest -q` before every commit to ensure tests pass.
- Follow PEP8 style with 4 spaces per indent and keep lines under 88 characters.
- Document any assumptions or limitations in the PR description.
- Do not add new dependencies without tests demonstrating the change.

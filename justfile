@sync:
    uv sync

@lock:
    uv lock

@upgrade:
    uv lock --upgrade

@lint:
    uv run ruff check .

@run:
    uv run python program.py

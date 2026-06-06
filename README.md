# rpi-kings

This script runs on a Raspberry Pi with a Sense HAT attached and scrolls
upcoming Seattle Kraken (`SEA`) game info across the LED matrix when a game
is about to start.

## Requirements

- A Raspberry Pi with a Sense HAT.
- Python 3.11 or newer.
- [`uv`](https://docs.astral.sh/uv/) for dependency management.
- [`just`](https://github.com/casey/just) (optional) for the helper recipes.

On Raspberry Pi OS the Sense HAT system libraries are easiest to install via
apt:

```sh
sudo apt install sense-hat
```

The PyPI `sense-hat` package is also listed in `pyproject.toml` so `uv sync`
will pull in the Python bindings.

## Setup

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/), then
sync the environment:

```sh
uv sync
```

This creates a `.venv` and installs the runtime + dev dependencies pinned in
`uv.lock`.

## Running

```sh
just run
# or, without just:
uv run python program.py
```

The script checks the NHL schedule for the configured team (`SEA`) and, if a
game is starting within the next 10 minutes, scrolls a summary across the
Sense HAT.

## Development

```sh
just lint           # ruff check
just lock           # refresh uv.lock
just upgrade        # refresh uv.lock with upgraded versions
```

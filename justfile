@sync:
    uv sync

# On a Raspberry Pi, the Sense HAT Python modules (`sense_hat`, `RTIMU`)
# come from apt and live in the system site-packages. Recreate the venv
# against system Python with `--system-site-packages` so they are importable.
@setup-pi:
    sudo apt install -y sense-hat
    rm -rf .venv
    uv venv --system-site-packages --python /usr/bin/python3
    uv sync

@lock:
    uv lock

@upgrade:
    uv lock --upgrade

@lint:
    uv run ruff check .

@run:
    uv run python program.py

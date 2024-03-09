@pip:
    uv pip compile requirements.in -o requirements.txt
    pip install -r requirements.txt

@lint:
    ruff check .
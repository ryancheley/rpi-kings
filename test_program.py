"""Offline checks for program.py. Run with `uv run python test_program.py`."""

import sys
import types
from datetime import timedelta

shown = []
sys.modules["sense_hat"] = types.SimpleNamespace(
    SenseHat=lambda: types.SimpleNamespace(
        show_message=lambda msg, **kw: shown.append(msg)
    )
)

import program  # noqa: E402

GAME = {"id": 1, "startTimeUTC": "2026-11-26T02:40:00Z"}
TEAM = {
    "placeName": {"default": "Seattle"},
    "commonName": {"default": "Kraken"},
    "abbrev": "SEA",
}
BOXSCORE = {
    "homeTeam": TEAM,
    "awayTeam": TEAM,
    "venue": {"default": "Climate Pledge Arena"},
}

program.get_current_week_schedule = lambda team_abbr: {"games": [GAME]}
program.get_boxscore = lambda game_id: BOXSCORE
program.get_standings = lambda: {"standings": []}

start = program.get_next_game_time(GAME)
assert start.strftime("%Y-%m-%d %H:%M %Z") == "2026-11-25 18:40 PST", start
assert program.team_name(TEAM) == "Seattle Kraken"


def scrolls_at(now) -> bool:
    shown.clear()
    program.NOW = now
    program.main()
    return bool(shown)


assert scrolls_at(start - timedelta(minutes=5))
assert "at 6:40 PM" in shown[0], shown[0]
assert not scrolls_at(start - timedelta(minutes=11))
assert not scrolls_at(start + timedelta(minutes=1))
assert not scrolls_at(
    start - timedelta(days=2, minutes=-5)
)  # same clock time, two days early
print("ok")

from datetime import datetime
import pytz

import httpx

from sense_hat import SenseHat

sense = SenseHat()

TEAM_ABBR = "SEA"
TIME_ZONE = "America/Los_Angeles"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/58.0.3029.110 Safari/537.3"
)

TODAY = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%Y-%m-%d")
NOW = datetime.now(pytz.timezone(TIME_ZONE))


def get_current_week_schedule(team_abbr: str) -> dict:
    url = f"https://api-web.nhle.com/v1/club-schedule/{team_abbr}/week/{TODAY}"
    response = httpx.get(url, headers={"user-agent": USER_AGENT})
    return response.json()


def get_boxscore(game_id: int) -> dict:
    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
    return httpx.get(url).json()


def get_standings() -> dict:
    url = f"https://api-web.nhle.com/v1/standings/{TODAY}"
    return httpx.get(url).json()


def get_next_game_time(game: dict) -> datetime:
    timezone = pytz.timezone(TIME_ZONE)
    naive = datetime.strptime(game["startTimeUTC"], DATETIME_FORMAT)
    return timezone.localize(naive)


def find_record(standings: dict, team_abbr: str) -> str | None:
    for team in standings.get("standings", []):
        if team.get("teamAbbrev", {}).get("default") == team_abbr:
            wins = team.get("wins")
            losses = team.get("losses")
            olt = team.get("otLosses")
            return f"{wins}-{losses}-{olt}"
    return None


def main():
    schedule = get_current_week_schedule(TEAM_ABBR)
    games = schedule.get("games", [])
    if not games:
        return

    game = games[0]
    boxscore = get_boxscore(game["id"])
    standings = get_standings()

    home = boxscore["homeTeam"]
    away = boxscore["awayTeam"]

    home_team = home["name"]["default"]
    home_record = find_record(standings, home["abbrev"])

    away_team = away["name"]["default"]
    away_record = find_record(standings, away["abbrev"])

    venue = boxscore["venue"]["default"]

    game_date = get_next_game_time(game)
    game_time_display = game_date.tzinfo.fromutc(game_date).time().strftime("%-I:%M %p")

    message = (
        f"The {home_team} ({home_record}) will be playing the "
        f"{away_team} ({away_record}) at {venue} at {game_time_display}"
    )

    time_diff = (game_date - NOW).seconds / 60
    if 10 >= time_diff >= 0:
        sense.show_message(message, scroll_speed=0.05)


if __name__ == "__main__":
    main()

from datetime import datetime
import pytz

import httpx

from sense_hat import SenseHat

sense = SenseHat()

TEAM_ABBR = "SEA"
TIME_ZONE = "America/Los_Angeles"

TODAY = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%Y-%m-%d")
NOW = datetime.now(pytz.timezone(TIME_ZONE))


def convert_utc_to_local(utc_time):
    local_timezone = pytz.timezone(TIME_ZONE)
    local_time = utc_time.astimezone(local_timezone)
    return local_time


def get_current_week_schedule(team_abbr: str):
    url = f"https://api-web.nhle.com/v1/club-schedule/{team_abbr}/week/{TODAY}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = httpx.get(url, headers=headers)
    return response.json()


def get_date_of_next_game(team_abbr: str, timezone=TIME_ZONE):
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"
    timezone = pytz.timezone(TIME_ZONE)
    schedule = get_current_week_schedule(team_abbr)
    game = schedule.get("games", [])
    next_game_time_utc = game[0].get("startTimeUTC")
    naive_datetime_object = datetime.strptime(next_game_time_utc, datetime_format)
    datetime_object_with_timezone = timezone.localize(naive_datetime_object)
    return datetime_object_with_timezone


def seconds_until_next_game():
    next_game = get_date_of_next_game(TEAM_ABBR)
    time_until_next_game = next_game - NOW

    return time_until_next_game.seconds


def get_game_id(team_abbr: str):
    schedule = get_current_week_schedule(team_abbr)
    game_id = schedule.get("games", [])[0].get("id")
    return game_id


def get_game_url(team_abbr: str):
    game_id = get_game_id(team_abbr)
    game_url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
    return game_url


def get_team_name(game_type: str):
    game_response = httpx.get(get_game_url(TEAM_ABBR)).json()
    team_name = game_response.get(game_type).get("name").get("default")
    return team_name


def get_team_abbreviation(game_type: str):
    game_response = httpx.get(get_game_url(TEAM_ABBR)).json()
    team_abbreviation = game_response.get(game_type).get("abbrev")
    return team_abbreviation


def get_record(team_abbr: str):
    url = f"https://api-web.nhle.com/v1/standings/{TODAY}"
    response = httpx.get(url).json()
    standings = response.get("standings")
    for team in standings:
        if team.get("teamAbbrev").get("default") == team_abbr:
            wins = team.get("wins")
            loses = team.get("losses")
            olt = team.get("otLosses")
            return f"{wins}-{loses}-{olt}"


def get_venue():
    game_response = httpx.get(get_game_url(TEAM_ABBR)).json()
    venue_name = game_response.get("venue").get("default")
    return venue_name


def main():
    home_abbreviation = get_team_abbreviation("homeTeam")
    home_team = get_team_name("homeTeam")
    home_record = get_record(home_abbreviation)

    away_abbreviation = get_team_abbreviation("awayTeam")
    away_team = get_team_name("awayTeam")
    away_record = get_record(away_abbreviation)

    venue = get_venue()

    game_date = get_date_of_next_game(TEAM_ABBR)
    game_time_display = (
        f"{game_date.tzinfo.fromutc(game_date).time().strftime('%-I:%M %p')}"
    )

    message = f"The {home_team} ({home_record}) will be playing the {away_team} ({away_record}) at {venue} at {game_time_display}"

    time_diff = seconds_until_next_game() / 60
    if 10 >= time_diff >= 0:
        sense.show_message(message, scroll_speed=0.05)


if __name__ == "__main__":
    main()

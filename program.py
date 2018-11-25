import requests
from sense_hat import SenseHat
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta



def main(team_id):
    sense = SenseHat()

    local_tz = pytz.timezone('America/Los_Angeles')
    utc_now = pytz.utc.localize(datetime.utcnow())
    now = utc_now.astimezone(local_tz)

    url = 'https://statsapi.web.nhl.com/api/v1/schedule?teamId={}'.format(team_id)
    r = requests.get(url)

    total_games = r.json().get('totalGames')
    if total_games >0:
        for i in range(total_games):
            game_time = (r.json().get('dates')[i].get('games')[0].get('gameDate'))
            away_team = (r.json().get('dates')[i].get('games')[0].get('teams').get('away').get('team').get('name'))
            home_team = (r.json().get('dates')[i].get('games')[0].get('teams').get('home').get('team').get('name'))
            away_team_id = (r.json().get('dates')[i].get('games')[0].get('teams').get('away').get('team').get('id'))
            home_team_id = (r.json().get('dates')[i].get('games')[0].get('teams').get('home').get('team').get('id'))
            game_time = datetime.strptime(game_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc).astimezone(local_tz)
            # The time_diff was added as a test
            time_diff = (now - game_time).total_seconds() / 60
            # These lines may be removed after testing
            minute_diff = relativedelta(now, game_time).minutes
            hour_diff = relativedelta(now, game_time).hours
            day_diff = relativedelta(now, game_time).days
            month_diff = relativedelta(now, game_time).months
            # end lines that can be removed
            game_time_hour = str(game_time.hour)
            game_time_minute = '0'+str(game_time.minute)
            game_time = game_time_hour+":"+game_time_minute[-2:]
            away_record = return_record(away_team_id)
            home_record = return_record(home_team_id)
            if 0 >= time_diff >= -10:
            #if month_diff == 0 and day_diff == 0 and hour_diff == 0 and 0 >= minute_diff >= -10:
                if home_team_id == team_id:
                    msg = 'The {} ({}) will be playing the {} ({}) at {}'.format(home_team, home_record, away_team, away_record ,game_time)
                else:
                    msg = 'The {} ({}) will be playing at the {} ({}) at {}'.format(home_team, home_record, away_team, away_record ,game_time)
                sense.show_message(msg, scroll_speed=0.05)

        game_ID = r.json().get('dates')[0].get('games')[0].get('gamePk')
        goal_checker(game_ID, team_id)


def goal_checker(game_id, team_id):
    url = 'http://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(game_id)
    r = requests.get(url)

    local_tz = pytz.timezone('America/Los_Angeles')
    utc_now = pytz.utc.localize(datetime.utcnow())
    now = utc_now.astimezone(local_tz)
    sense = SenseHat()


    scoring_plays = r.json().get('liveData').get('plays').get('scoringPlays')

    for i in range(len(scoring_plays)):
        goal_team_id = r.json().get('liveData').get('plays').get('allPlays')[scoring_plays[i]].get('team').get('id')
        goal_ts = r.json().get('liveData').get('plays').get('allPlays')[scoring_plays[i]].get('about').get('dateTime')
        goal_ts = datetime.strptime(goal_ts, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc).astimezone(local_tz)
        minute_diff = relativedelta(now, goal_ts).minutes
        hour_diff = relativedelta(now, goal_ts).hours
        day_diff = relativedelta(now, goal_ts).days
        month_diff = relativedelta(now, goal_ts).months
        goal_ts_hour = str(goal_ts.hour)
        goal_ts_minute = '0'+str(goal_ts.minute)
        goal_ts = goal_ts_hour+":"+goal_ts_minute[-2:]
        if month_diff == 0 and day_diff == 0 and hour_diff == 0 and 2 >= minute_diff >= 0:
            if goal_team_id == team_id:            
                goal_msg = 'GOAL!!!! '+r.json().get('liveData').get('plays').get('allPlays')[scoring_plays[i]].get('result').get('description')
                sense.show_message(goal_msg, scroll_speed=0.05)


def return_record(team_id):
    standings_url = 'https://statsapi.web.nhl.com/api/v1/teams/{}/stats'.format(team_id)
    r = requests.get(standings_url)
    wins = (r.json().get('stats')[0].get('splits')[0].get('stat').get('wins'))
    losses = (r.json().get('stats')[0].get('splits')[0].get('stat').get('losses'))
    otl = (r.json().get('stats')[0].get('splits')[0].get('stat').get('ot'))
    record = str(wins)+'-'+str(losses)+'-'+str(otl)
    return record


if __name__ == '__main__':
    main(26) # This is the code for the LA Kings; the ID can be found here: https://statsapi.web.nhl.com/api/v1/teams/

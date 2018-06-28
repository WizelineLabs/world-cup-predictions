import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "world_cup_predictions.settings")

import django
django.setup()

from api.models import Team, HistoricalGame, WorldCupGame, User, Vote, Prediction, Group
from model.worldcup_predictor import predict_worldcup, get_defense_capabilities
from datetime import datetime as dt
import pandas as pd
import pytz

date_format = '%Y-%m-%dT%H:%M:%S'
best16 = {'A1':'Uruguay','A2':'Russia','B1':'Spain','B2':'Portugal',
         'C1':'France','C2':'Denmark','D1':'Croatia','D2':'Argentina',
         'E1':'Brazil','E2':'Switzerland','F1':'Sweden','F2':'Mexico',
         'G1':'Belgium','G2':'England','H1':'Colombia','H2':'Japan'}
round_16_matches = [
    {
        'round': '16',
        'home_team': 9,
        'away_team': 13,
        'date': '2018-06-30T14:00:00',
    },
    {
        'round': '16',
        'home_team': 4,
        'away_team': 5,
        'date': '2018-06-30T18:00:00',
    },
    {
        'round': '16',
        'home_team': 6,
        'away_team': 1,
        'date': '2018-07-01T14:00:00',
    },
    {
        'round': '16',
        'home_team': 15,
        'away_team': 12,
        'date': '2018-07-01T18:00:00',
    },
    {
        'round': '16',
        'home_team': 17,
        'away_team': 22,
        'date': '2018-07-02T14:00:00',
    },
    {
        'round': '16',
        'home_team': 25,
        'away_team': 32,
        'date': '2018-07-02T18:00:00',
    },
    {
        'round': '16',
        'home_team': 23,
        'away_team': 18,
        'date': '2018-07-03T14:00:00',
    },
    {
        'round': '16',
        'home_team': 31,
        'away_team': 28,
        'date': '2018-07-03T18:00:00',
    }
]
def populate_matches(matches):
    for match in matches:
        match['date'] = dt.strptime(match['date'], date_format)
        match['date'] = match['date'].replace(tzinfo=pytz.UTC)
        WorldCupGame.objects.create(
            home_team_id=match['home_team'],
            away_team_id=match['away_team'],
            round=match['round'],
            date=match['date'])

def update_winning_probabilities():
  previous_games = [historical_game.to_dict() for historical_game in HistoricalGame.objects.all()] + [worldcup_game.to_dict() for worldcup_game in WorldCupGame.objects.exclude(home_score__isnull=True)]
  history = pd.DataFrame.from_records(previous_games)
  defense = get_defense_capabilities(history)
  world_cup_predictions = predict_worldcup(history, defense, best16)
  pass_round16 = world_cup_predictions[1][1]
  pass_quarters = world_cup_predictions[1][2]
  pass_semis = world_cup_predictions[1][3]
  champion = world_cup_predictions[1][4]
  for team in Team.objects.all():
     team.pass_round16_prob=pass_round16[team.name]
     team.pass_quarters_prob=pass_quarters[team.name]
     team.pass_semi_prob=pass_semis[team.name]
     team.pass_final_prob=champion[team.name]
     team.save()


populate_matches(round_16_matches)
update_winning_probabilities()
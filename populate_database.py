import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "world_cup_predictions.settings")

import django
django.setup()

from api.models import Team, HistoricalGame, WorldCupGame, User, Vote, Prediction, Group
from model.worldcup_predictor import predict_group_match, predict_worldcup, fetch_matches, get_defense_capabilities, advance_to_knockout
from predict_matches import populate_group_predictions, populate_knockout_predictions
from datetime import datetime as dt
import pytz
import numpy as np
import pandas as pd
from django.contrib.auth import get_user_model

threshold = '2016-06-14'
date_format = '%Y-%m-%dT%H:%M:%S'
groups = {
    'Russia': 1,
    'Saudi Arabia': 1,
    'Egypt': 1,
    'Uruguay': 1,
    'Portugal': 2,
    'Spain': 2,
    'Morocco': 2,
    'Iran': 2,
    'France': 3,
    'Australia': 3,
    'Peru': 3,
    'Denmark': 3,
    'Argentina': 4,
    'Iceland': 4,
    'Croatia': 4,
    'Nigeria': 4,
    'Brazil': 5,
    'Switzerland': 5,
    'Costa Rica': 5,
    'Serbia': 5,
    'Germany': 6,
    'Mexico': 6,
    'Sweden': 6,
    'Korea Republic': 6,
    'Belgium': 7,
    'Panama': 7,
    'Tunisia': 7,
    'England': 7,
    'Poland': 8,
    'Senegal': 8,
    'Colombia': 8,
    'Japan': 8
}
group_matches = [
    {
        'round': 'A',
        'home_team': 1,
        'away_team': 2,
        'date': '2018-06-14T15:00:00',
    },
    {
        'round': 'A',
        'home_team': 3,
        'away_team': 4,
        'date': '2018-06-15T12:00:00',
    },
    {
        'round': 'A',
        'home_team': 1,
        'away_team': 3,
        'date': '2018-06-19T18:00:00',
    },
    {
        'round': 'A',
        'home_team': 4,
        'away_team': 2,
        'date': '2018-06-20T15:00:00',
    },
    {
        'round': 'A',
        'home_team': 4,
        'away_team': 1,
        'date': '2018-06-25T14:00:00',
    },
    {
        'round': 'A',
        'home_team': 2,
        'away_team': 3,
        'date': '2018-06-25T14:00:00',
    },
    {
        'round': 'B',
        'home_team': 5,
        'away_team': 6,
        'date': '2018-06-15T18:00:00',
    },
    {
        'round': 'B',
        'home_team': 7,
        'away_team': 8,
        'date': '2018-06-15T15:00:00',
    },
    {
        'round': 'B',
        'home_team': 5,
        'away_team': 7,
        'date': '2018-06-20T12:00:00',
    },
    {
        'round': 'B',
        'home_team': 8,
        'away_team': 6,
        'date': '2018-06-20T18:00:00',
    },
    {
        'round': 'B',
        'home_team': 8,
        'away_team': 5,
        'date': '2018-06-25T18:00:00',
    },
    {
        'round': 'B',
        'home_team': 6,
        'away_team': 7,
        'date': '2018-06-25T18:00:00',
    },
    {
        'round': 'C',
        'home_team': 9,
        'away_team': 10,
        'date': '2018-06-16T10:00:00',
    },
    {
        'round': 'C',
        'home_team': 11,
        'away_team': 12,
        'date': '2018-06-16T16:00:00',
    },
    {
        'round': 'C',
        'home_team': 9,
        'away_team': 11,
        'date': '2018-06-21T15:00:00',
    },
    {
        'round': 'C',
        'home_team': 12,
        'away_team': 10,
        'date': '2018-06-21T12:00:00',
    },
    {
        'round': 'C',
        'home_team': 12,
        'away_team': 9,
        'date': '2018-06-26T14:00:00',
    },
    {
        'round': 'C',
        'home_team': 10,
        'away_team': 11,
        'date': '2018-06-26T15:00:00',
    },
    {
        'round': 'D',
        'home_team': 13,
        'away_team': 14,
        'date': '2018-06-16T13:00:00',
    },
    {
        'round': 'D',
        'home_team': 15,
        'away_team': 16,
        'date': '2018-06-16T19:00:00',
    },
    {
        'round': 'D',
        'home_team': 13,
        'away_team': 15,
        'date': '2018-06-21T18:00:00',
    },
    {
        'round': 'D',
        'home_team': 16,
        'away_team': 14,
        'date': '2018-06-22T15:00:00',
    },
    {
        'round': 'D',
        'home_team': 16,
        'away_team': 13,
        'date': '2018-06-26T18:00:00',
    },
    {
        'round': 'D',
        'home_team': 14,
        'away_team': 15,
        'date': '2018-06-26T18:00:00',
    },
    {
        'round': 'E',
        'home_team': 17,
        'away_team': 18,
        'date': '2018-06-17T18:00:00',
    },
    {
        'round': 'E',
        'home_team': 19,
        'away_team': 20,
        'date': '2018-06-17T12:00:00',
    },
    {
        'round': 'E',
        'home_team': 17,
        'away_team': 19,
        'date': '2018-06-22T12:00:00',
    },
    {
        'round': 'E',
        'home_team': 20,
        'away_team': 18,
        'date': '2018-06-22T18:00:00',
    },
    {
        'round': 'E',
        'home_team': 20,
        'away_team': 17,
        'date': '2018-06-27T18:00:00',
    },
    {
        'round': 'E',
        'home_team': 18,
        'away_team': 19,
        'date': '2018-06-27T18:00:00',
    },
    {
        'round': 'F',
        'home_team': 21,
        'away_team': 22,
        'date': '2018-06-17T15:00:00',
    },
    {
        'round': 'F',
        'home_team': 23,
        'away_team': 24,
        'date': '2018-06-18T12:00:00',
    },
    {
        'round': 'F',
        'home_team': 21,
        'away_team': 23,
        'date': '2018-06-23T18:00:00',
    },
    {
        'round': 'F',
        'home_team': 24,
        'away_team': 22,
        'date': '2018-06-23T15:00:00',
    },
    {
        'round': 'F',
        'home_team': 24,
        'away_team': 21,
        'date': '2018-06-27T14:00:00',
    },
    {
        'round': 'F',
        'home_team': 22,
        'away_team': 23,
        'date': '2018-06-27T12:00:00',
    },
    {
        'round': 'G',
        'home_team': 25,
        'away_team': 26,
        'date': '2018-06-18T15:00:00',
    },
    {
        'round': 'G',
        'home_team': 27,
        'away_team': 28,
        'date': '2018-06-18T18:00:00',
    },
    {
        'round': 'G',
        'home_team': 25,
        'away_team': 27,
        'date': '2018-06-23T12:00:00',
    },
    {
        'round': 'G',
        'home_team': 28,
        'away_team': 26,
        'date': '2018-06-24T12:00:00',
    },
    {
        'round': 'G',
        'home_team': 28,
        'away_team': 25,
        'date': '2018-06-28T18:00:00',
    },
    {
        'round': 'G',
        'home_team': 26,
        'away_team': 27,
        'date': '2018-06-28T18:00:00',
    },
    {
        'round': 'H',
        'home_team': 29,
        'away_team': 30,
        'date': '2018-06-19T15:00:00',
    },
    {
        'round': 'H',
        'home_team': 31,
        'away_team': 32,
        'date': '2018-06-19T12:00:00',
    },
    {
        'round': 'H',
        'home_team': 29,
        'away_team': 31,
        'date': '2018-06-24T15:00:00',
    },
    {
        'round': 'H',
        'home_team': 32,
        'away_team': 30,
        'date': '2018-06-24T18:00:00',
    },
    {
        'round': 'H',
        'home_team': 32,
        'away_team': 29,
        'date': '2018-06-28T14:00:00',
    },
    {
        'round': 'H',
        'home_team': 30,
        'away_team': 31,
        'date': '2018-06-28T14:00:00',
    },
]
flags = [
    {
        'id': 1,
        'code': 'ru',
        'name': 'Russia',
    },
    {
        'id': 2,
        'code': 'sa',
        'name': 'Saudi Arabia',
    },
    {
        'id': 3,
        'code': 'eg',
        'name': 'Egypt',
    },
    {
        'id': 4,
        'code': 'uy',
        'name': 'Uruguay',
    },
    {
        'id': 5,
        'code': 'pt',
        'name': 'Portugal',
    },
    {
        'id': 6,
        'code': 'es',
        'name': 'Spain',
    },
    {
        'id': 7,
        'code': 'ma',
        'name': 'Morocco',
    },
    {
        'id': 8,
        'code': 'ir',
        'name': 'Iran',
    },
    {
        'id': 9,
        'code': 'fr',
        'name': 'France',
    },
    {
        'id': 10,
        'code': 'au',
        'name': 'Australia',
    },
    {
        'id': 11,
        'code': 'pe',
        'name': 'Peru',
    },
    {
        'id': 12,
        'code': 'dk',
        'name': 'Denmark',
    },
    {
        'id': 13,
        'code': 'ar',
        'name': 'Argentina',
    },
    {
        'id': 14,
        'code': 'is',
        'name': 'Iceland',
    },
    {
        'id': 15,
        'code': 'hr',
        'name': 'Croatia',
    },
    {
        'id': 16,
        'code': 'ng',
        'name': 'Nigeria',
    },
    {
        'id': 17,
        'code': 'br',
        'name': 'Brazil',
    },
    {
        'id': 18,
        'code': 'ch',
        'name': 'Switzerland',
    },
    {
        'id': 19,
        'code': 'cr',
        'name': 'Costa Rica',
    },
    {
        'id': 20,
        'code': 'rs',
        'name': 'Serbia',
    },
    {
        'id': 21,
        'code': 'de',
        'name': 'Germany',
    },
    {
        'id': 22,
        'code': 'mx',
        'name': 'Mexico',
    },
    {
        'id': 23,
        'code': 'se',
        'name': 'Sweden',
    },
    {
        'id': 24,
        'code': 'kr',
        'name': 'Korea Republic',
    },
    {
        'id': 25,
        'code': 'be',
        'name': 'Belgium',
    },
    {
        'id': 26,
        'code': 'pa',
        'name': 'Panama',
    },
    {
        'id': 27,
        'code': 'tn',
        'name': 'Tunisia',
    },
    {
        'id': 28,
        'code': 'gb-eng',
        'name': 'England',
    },
    {
        'id': 29,
        'code': 'pl',
        'name': 'Poland',
    },
    {
        'id': 30,
        'code': 'sn',
        'name': 'Senegal',
    },
    {
        'id': 31,
        'code': 'co',
        'name': 'Colombia',
    },
    {
        'id': 32,
        'code': 'jp',
        'name': 'Japan',
    },
]

def create_superuser():
    User = get_user_model()
    try:
        super_user = User.objects.filter(email='admin@wizeline.com')[0]
    except:
        User.objects.create_superuser('admin', 'admin@wizeline.com', 'mosalah22abotrika')

def populate_groups():
    for i in range(8):
        group = Group(group_label=chr(ord('A') + i))
        group.save()


def populate_historical_matches(matches):
    for match in matches.itertuples(index=True, name='Pandas'):
        game = HistoricalGame(
            home_team=getattr(match, 'home_team'),
            away_team=getattr(match, 'away_team'),
            home_score=getattr(match, 'home_score'),
            away_score=getattr(match, 'away_score'))
        game.save()

def populate_flag_codes():
    for item in flags:
        team = Team.objects.get(name=item['name'])
        team.flag_code = item['code']
        team.save()
def populate_teams(world_cup_predictions):
    pass_group = world_cup_predictions[0]
    pass_round16 = world_cup_predictions[1][1]
    pass_quarters = world_cup_predictions[1][2]
    pass_semis = world_cup_predictions[1][3]
    champion = world_cup_predictions[1][4]

    credible_round_16 = advance_to_knockout(
        pass_group, pd.read_csv('./records.csv', index_col=0))
    index = 0
    for team, probs in pass_group.items():
        Team.objects.create(
            name=team,
            group_label=Group.objects.get(pk=int(index/4)+1),
            pass_group_winner_prob=probs['1'],
            pass_group_runner_prob=probs['2'],
            pass_round16_prob=pass_round16[team],
            pass_quarters_prob=pass_quarters[team],
            pass_semi_prob=pass_semis[team],
            pass_final_prob=champion[team])
        index = index + 1
    for key, value in credible_round_16.items():
        team = Team.objects.get(name=value)
        team.shaded = True
        if key.endswith('1'):
            team.first = True
        else:
            team.second = True
        team.save()
    populate_flag_codes()


def populate_worldCup_matches(matches):
    for match in matches:
        match['date'] = dt.strptime(match['date'], date_format)
        match['date'] = match['date'].replace(tzinfo=pytz.UTC)
        WorldCupGame.objects.create(
            home_team_id=match['home_team'],
            away_team_id=match['away_team'],
            round=match['round'],
            date=match['date'])


np.random.seed(10101)

create_superuser()
games = WorldCupGame.objects.all()
teams = Team.objects.all()
groups = Group.objects.all()
if not games or not teams or not groups:
    historical_matches = fetch_matches('results.csv', threshold)
    defense = get_defense_capabilities(historical_matches)
    world_cup_predictions = predict_worldcup(historical_matches, defense)
    populate_groups()
    populate_historical_matches(historical_matches)
    populate_teams(world_cup_predictions)
    populate_worldCup_matches(group_matches)
    populate_flag_codes()

group_matches = WorldCupGame.objects.filter(pk__lte=48)
knockout_matches = WorldCupGame.objects.filter(pk__gt=48)
populate_group_predictions(group_matches)
populate_knockout_predictions(knockout_matches)

print('Database Population Done')

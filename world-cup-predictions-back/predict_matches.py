import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "world_cup_predictions.settings")

import django
django.setup()

from api.models import Team, HistoricalGame, WorldCupGame, User, Vote, Prediction, Group
from model.worldcup_predictor import predict_group_match, win_knockout_match, fetch_matches, get_defense_capabilities
from datetime import datetime as dt
import numpy as np
import pandas as pd

threshold = '2016-06-14'
historical_matches = fetch_matches('results.csv', threshold)
defense = get_defense_capabilities(historical_matches)

def populate_group_predictions(group_matches):
  for match in group_matches:
    try:
      prediction_outcome = predict_group_match(str(match.home_team), str(match.away_team), historical_matches, defense)
    except:
      pass
    try:
      prediction = Prediction.objects.get(pk=match.id)
      prediction.home_win = prediction_outcome['win']
      prediction.away_win = prediction_outcome['lose']
      prediction.draw = prediction_outcome['draw']
      prediction.save()
    except:
      Prediction.objects.create(
        game_id=match.id,
        home_win=prediction_outcome['win'],
        away_win=prediction_outcome['lose'],
        draw=prediction_outcome['draw']
      )

def populate_knockout_predictions(knockout_matches):
  for match in knockout_matches:
    try:
      home_win = win_knockout_match(str(match.home_team), str(match.away_team), historical_matches, defense)
    except:
      pass
    try:
      prediction = Prediction.objects.get(pk=match.id)
      prediction.home_win = home_win
      prediction.away_win = 1 - home_win
      prediction.draw = 0
      prediction.save()
    except:
      Prediction.objects.create(
        game_id=match.id,
        home_win=home_win,
        away_win=(1-home_win),
        draw=0
      )
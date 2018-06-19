import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "world_cup_predictions.settings")

import django
django.setup()

from api.models import Team, HistoricalGame, WorldCupGame, User, Vote, Prediction, Group

def get_or_create_Paul():
  try:
    paul = User.objects.filter(email='paul.prediction@wizeline.com')[0]
    return paul.id
  except:
    paul = User.objects.create(first_name='Paul', last_name='Prediction', email='paul.prediction@wizeline.com')
    return paul.id

def get_paul_choice(home_win, away_win, draw):
   if home_win > away_win and home_win > draw:
     return 'H'
   elif away_win > home_win and away_win > draw:
     return 'A'
   else:
     return 'D'
def create_votes_from_predictions(predictions):
  paul_id = get_or_create_Paul()
  paul = User.objects.get(pk=paul_id)
  for prediction in predictions:
    try:
      vote = Vote.objects.filter(user=paul,game=prediction.game)[0]
      pass
    except:
      paul_choice = get_paul_choice(prediction.home_win,prediction.away_win, prediction.draw)
      Vote.objects.create(user=paul, game=prediction.game, choice=paul_choice)


predictions = Prediction.objects.all()
create_votes_from_predictions(predictions)
print('Paul User updated')
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "world_cup_predictions.settings")

import django
django.setup()

from api.models import Team, HistoricalGame, WorldCupGame, User, Vote, Prediction, Group
from datetime import datetime as dt
from django.utils import timezone

ONE_CORRECT_VOTE_SCORE = 10
HOME_WIN = 'H'
AWAY_WIN = 'A'
DRAW = 'D'

def get_actual_result(game):
  home_score = game.home_score
  away_score = game.away_score
  if home_score > away_score:
    return HOME_WIN
  elif home_score < away_score:
    return AWAY_WIN
  else:
    return DRAW

def evaluate_votes(votes):
  for vote in votes:
    if vote.correct is None:
      game = vote.game
      actual_result = get_actual_result(game)
      if vote.choice == actual_result:
        vote.correct = True
      else:
        vote.correct = False
      vote.save()

def update_scores(users):
  for user in users:
    correct_votes = user.votes.filter(correct=True).count()
    correct_score = correct_votes * ONE_CORRECT_VOTE_SCORE
    if user.score != correct_score:
      print('score of user %s is not correct, updating' % (user.id))
      user.score = correct_score
      user.save()

played_games_votes = Vote.objects.filter(game__date__lte=timezone.now())
evaluate_votes(played_games_votes)
users = User.objects.all()
update_scores(users)
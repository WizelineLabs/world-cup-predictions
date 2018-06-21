from django.db import models
from django.contrib.auth.models import AbstractUser
import logging

logger = logging.getLogger('api.models')
# Create your models here.
HOME_WIN = 'H'
AWAY_WIN = 'A'
DRAW = 'D'
ONE_CORRECT_VOTE_SCORE = 10
class Group(models.Model):
  GROUP_A = 'A'
  GROUP_B = 'B'
  GROUP_C = 'C'
  GROUP_D = 'D'
  GROUP_E = 'E'
  GROUP_F = 'F'
  GROUP_G = 'G'
  GROUP_H = 'H'

  GROUP_CHOICES = (
    (GROUP_A, 'A'),
    (GROUP_B, 'B'),
    (GROUP_C, 'C'),
    (GROUP_D, 'D'),
    (GROUP_E, 'E'),
    (GROUP_F, 'F'),
    (GROUP_G, 'G'),
    (GROUP_H, 'H')
  )
  group_label = models.CharField(
    null=True,
    max_length=1,
    choices=GROUP_CHOICES,
  )
  def __str__(self):
    return self.group_label

class Team(models.Model):
  name = models.CharField(max_length=200, db_index=True)
  group_label = models.ForeignKey(Group, related_name='teams', on_delete=models.CASCADE, null=True)
  rank = models.IntegerField(null=True)
  points = models.IntegerField(default=0)
  pass_group_winner_prob = models.FloatField(null=True)
  pass_group_runner_prob = models.FloatField(null=True)
  pass_round16_prob = models.FloatField(null=True)
  pass_quarters_prob = models.FloatField(null=True)
  pass_semi_prob = models.FloatField(null=True)
  pass_final_prob = models.FloatField(null=True)
  shaded = models.BooleanField(default=False)
  first = models.BooleanField(default=False)
  second = models.BooleanField(default=False)
  flag_code = models.CharField(max_length=10, null=True)
  def __str__(self):
    return '%s' % (self.name)

class HistoricalGame(models.Model):
  home_team = models.CharField(max_length=200)
  away_team = models.CharField(max_length=200)
  home_score = models.IntegerField(default=0)
  away_score = models.IntegerField(default=0)

  def to_dict(self):
    return {
      'home_team': str(self.home_team),
      'away_team': str(self.away_team),
      'home_score': self.home_score,
      'away_score': self.away_score
    }

class WorldCupGame(models.Model):
    home_team = models.ForeignKey(Team, related_name='game_home', on_delete=models.CASCADE, null=True)
    away_team = models.ForeignKey(Team, related_name='game_away', on_delete=models.CASCADE, null=True)
    home_score = models.IntegerField(null=True)
    away_score = models.IntegerField(null=True)
    round = models.CharField(max_length=50, null=True, db_index=True)
    date = models.DateTimeField(null=True)
    def __str__(self):
        return '%s(%s) - %s(%s)' % (self.home_team, self.home_score, self.away_team, self.away_score)

    def save(self, *args, **kwargs):
      if(self.home_score is not None and self.away_score is not None):
        update_users_scores(self)
      super(WorldCupGame, self).save(*args, **kwargs)
    
    def to_dict(self):
      return {
        'home_team': str(self.home_team),
        'away_team': str(self.away_team),
        'home_score': self.home_score,
        'away_score': self.away_score
      }


class Prediction(models.Model):
  game = models.OneToOneField(WorldCupGame, on_delete=models.CASCADE, primary_key=True, )
  home_win = models.FloatField(default=0)
  away_win = models.FloatField(default=0)
  draw = models.FloatField(default=0)

class User(AbstractUser):
  avatar = models.CharField(null=True, max_length=200)
  score = models.IntegerField(default=0)
  winner_choice = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
  following = models.ManyToManyField('self', related_name='followers', symmetrical=False)
  def __str__(self):
    return '%s' % (self.email)

class Vote(models.Model):
  HOME_WIN = 'H'
  AWAY_WIN = 'A'
  DRAW = 'D'
  RESULT_CHOICES = (
    (HOME_WIN, 'H'),
    (AWAY_WIN, 'A'),
    (DRAW, 'D'),
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
  game = models.ForeignKey(WorldCupGame, on_delete=models.CASCADE)
  choice = models.CharField(
    null=True,
    max_length=1,
    choices=RESULT_CHOICES,
    )
  correct = models.NullBooleanField(null=True)

  class Meta:
    unique_together = (("user", "game"),)


def update_users_scores(instance):
  if instance.home_score is not None and instance.away_score is not None:
    actual_result = get_actual_result(instance)
    game_id = instance.id
    users = User.objects.all()
    for user in users:
      try:
        user_vote = user.votes.get(game__id=game_id)
        correct = evaluate_vote(user_vote, actual_result)
        if correct:
          user.score += ONE_CORRECT_VOTE_SCORE
          user.save()
      except:
        pass

def evaluate_vote(vote, actual_result):
  if vote.correct is None:
    if vote.choice == actual_result:
      vote.correct = True
    else:
      vote.correct = False
    vote.save()
    return vote.correct
  else:
    return False

def get_actual_result(game):
  home_score = game.home_score
  away_score = game.away_score
  if home_score > away_score:
    return HOME_WIN
  elif home_score < away_score:
    return AWAY_WIN
  else:
    return DRAW
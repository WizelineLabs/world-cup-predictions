from django.db import models

# Create your models here.

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

class Team(models.Model):
  name = models.CharField(max_length=200, db_index=True)
  group_label = models.ForeignKey(Group, related_name='teams', on_delete=models.CASCADE, null=True)
  rank = models.IntegerField(null=True)
  points = models.IntegerField(default=0)
  pass_group_1st_prob = models.FloatField(null=True)
  pass_group_2nd_prob = models.FloatField(null=True)
  pass_round16_prob = models.FloatField(null=True)
  pass_quarters_prob = models.FloatField(null=True)
  pass_semi_prob = models.FloatField(null=True)
  pass_final_prob = models.FloatField(null=True)
  def __str__(self):
    return '%s' % (self.name)

class HistoricalGame(models.Model):
  home_team = models.CharField(max_length=200)
  away_team = models.CharField(max_length=200)
  home_score = models.IntegerField(default=0)
  away_score = models.IntegerField(default=0)

class WorldCupGame(models.Model):
    home_team = models.ForeignKey(Team, related_name='game_home', on_delete=models.CASCADE, null=True)
    away_team = models.ForeignKey(Team, related_name='game_away', on_delete=models.CASCADE, null=True)
    home_score = models.IntegerField(null=True)
    away_score = models.IntegerField(null=True)
    round = models.CharField(max_length=50, null=True, db_index=True)
    date = models.DateTimeField(null=True)
    def __str__(self):
        return '%s(%s) - %s(%s)' % (self.home_team, self.home_score, self.away_team, self.away_score)

class Prediction(models.Model):
  game = models.OneToOneField(WorldCupGame, on_delete=models.CASCADE, primary_key=True, )
  home_win = models.FloatField(default=0)
  away_win = models.FloatField(default=0)
  draw = models.FloatField(default=0)

class User(models.Model):
  email = models.CharField(max_length=200, db_index=True)
  name = models.CharField(max_length=200, null=True)
  score = models.IntegerField(default=0)
  winner_choice = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
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
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  game = models.ForeignKey(WorldCupGame, on_delete=models.CASCADE)
  choice = models.CharField(
    null=True,
    max_length=1,
    choices=RESULT_CHOICES,
    )
  correct = models.NullBooleanField(null=True)

  class Meta:
    unique_together = (("user", "game"),)
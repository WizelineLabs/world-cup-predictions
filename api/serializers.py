from rest_framework import serializers
from api.models import User, HistoricalGame, WorldCupGame, Prediction, Vote, Group, Team

class HistoricalGameSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    # highlight = serializers.HyperlinkedIdentityField(
    #     view_name='snippet-highlight', format='html')

    class Meta:
        model = HistoricalGame
        fields = ('id', 'home_team', 'away_team', 'home_score', 'away_score')

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.CharField(source='group_label.group_label')
    class Meta:
        model = Team
        fields = ('id', 'name', 'group', 'rank', 'points',
          'pass_group_winner_prob', 'pass_group_runner_prob', 'pass_round16_prob', 
          'pass_quarters_prob', 'pass_semi_prob', 'pass_final_prob', 'shaded')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    teams = serializers.StringRelatedField(many=True)
    class Meta:
        model = Group
        fields = ('id', 'group_label', 'teams')

class WorldCupGameSerializer(serializers.HyperlinkedModelSerializer):
    home = serializers.CharField(source='home_team.name')
    away = serializers.CharField(source='away_team.name')
    class Meta:
        model = WorldCupGame
        fields = ('id', 'home', 'away', 'home_score', 'away_score', 'round', 'date')

class PredictionSerializer(serializers.HyperlinkedModelSerializer):
    game_id = serializers.IntegerField(source='game.id')
    class Meta:
        model = Prediction
        fields = ('game_id', 'home_win', 'away_win', 'draw')

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    game_id = serializers.IntegerField(source='game.id')
    class Meta:
        model = Vote
        fields = ('user_id', 'game_id', 'choice', 'correct')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'score' 'winner_choice')

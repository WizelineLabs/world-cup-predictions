from rest_framework import serializers
from api.models import User, HistoricalGame, WorldCupGame, Prediction, Vote, Group, Team
from datetime import timedelta
from django.utils import timezone

class HistoricalGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalGame
        fields = ('id', 'home_team', 'away_team', 'home_score', 'away_score')

class TeamSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group_label.group_label')
    class Meta:
        model = Team
        fields = ('id', 'name', 'group', 'rank', 'points',
          'pass_group_winner_prob', 'pass_group_runner_prob', 'pass_round16_prob', 
          'pass_quarters_prob', 'pass_semi_prob', 'pass_final_prob', 'shaded', 'flag_code')

class GroupSerializer(serializers.ModelSerializer):
    teams = serializers.StringRelatedField(many=True)
    class Meta:
        model = Group
        fields = ('id', 'group_label', 'teams')

class WorldCupGameSerializer(serializers.ModelSerializer):
    home = serializers.CharField(source='home_team.name')
    away = serializers.CharField(source='away_team.name')
    home_flag = serializers.CharField(source='home_team.flag_code')
    away_flag = serializers.CharField(source='away_team.flag_code')
    class Meta:
        model = WorldCupGame
        fields = ('id', 'home', 'home_flag', 'away', 'away_flag', 'home_score', 'away_score', 'round', 'date')

class PredictionSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField(source='game.id')
    class Meta:
        model = Prediction
        fields = ('game_id', 'home_win', 'away_win', 'draw')

class VoteSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField(source='game.id')
    class Meta:
        model = Vote
        fields = ('id', 'game_id', 'choice', 'correct')

class UserSerializer(serializers.ModelSerializer):
    total_votes = serializers.SerializerMethodField()
    correct_votes = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    finished_matches = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'score', 'avatar', 'winner_choice', 'total_votes', 'correct_votes', 'rank' , 'finished_matches')

    def get_total_votes(self, obj):
        return obj.votes.all().count()
    def get_correct_votes(self, obj):
        return obj.votes.filter(correct=True).count()
    def get_rank(self, obj):
        return (User.objects.filter(score__gt=obj.score).count() + 1)
    def get_finished_matches(self, obj):
        return WorldCupGame.objects.filter(date__lte=timezone.now()-timedelta(hours=2, minutes=30)).count()

class LeaderboardSerializer(serializers.ModelSerializer):
    total_votes = serializers.SerializerMethodField()
    correct_votes = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    class Meta :
        model = User
        fields = ('first_name', 'last_name', 'score', 'avatar','total_votes', 'correct_votes', 'rank')
    
    def get_total_votes(self, obj):
        return obj.votes.all().count()
    def get_correct_votes(self, obj):
        return obj.votes.filter(correct=True).count()
    def get_rank(self, obj):
        return (User.objects.filter(score__gt=obj.score).count() + 1)

class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )

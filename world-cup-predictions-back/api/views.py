from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from requests.exceptions import HTTPError

from social_django.utils import psa

import pandas as pd
import logging

from api.models import HistoricalGame, Team, Group, WorldCupGame, Prediction, Vote, User
from api.serializers import HistoricalGameSerializer, TeamSerializer, GroupSerializer, WorldCupGameSerializer, PredictionSerializer, VoteSerializer, UserSerializer, SocialSerializer, LeaderboardSerializer, TrendSerializer
from model.worldcup_predictor import predict_group_match, get_defense_capabilities, win_knockout_match, fetch_matches
#Comment this import if it is the first time you are running the project in order to let the migrations run ok
from update_paul_user import get_paul_choice

class HistoricalGameViewSet(viewsets.ModelViewSet):
    queryset = HistoricalGame.objects.all()
    serializer_class = HistoricalGameSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.order_by('-pass_final_prob','-pass_semi_prob','-pass_quarters_prob','-pass_round16_prob','-pass_group_runner_prob','-pass_group_winner_prob')
    serializer_class = TeamSerializer
    http_method_names = ['get']

class TopContendersViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.order_by('-pass_final_prob')[:5]
    serializer_class = TeamSerializer
    http_method_names = ['get']

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ['get']

class WorldCupGameViewSet(viewsets.ModelViewSet):
    queryset = WorldCupGame.objects.all()
    serializer_class = WorldCupGameSerializer
    http_method_names = ['get']

class PredictionViewSet(viewsets.ModelViewSet):
    #queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = (permissions.IsAuthenticated, )
    http_method_names = ['get']
    def get_queryset(self):
        threshold = timezone.now()
        finsihed_or_in_progress_games = WorldCupGame.objects.filter(date__lte=threshold)
        for game in finsihed_or_in_progress_games:
            try:
                game_prediction = Prediction.objects.get(game__id=game.id)
                pass
            except:
                make_prediction(game)
        return Prediction.objects.filter(game__date__lte=threshold)

class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated, )
    http_method_names = ['get']
    def get_queryset(self):
        return self.request.user.votes.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    http_method_names = ['get']
    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)

@api_view(http_method_names=['POST'])
@permission_classes([permissions.IsAuthenticated])
def choose_winner(request):
    now = timezone.now()
    world_cup_start = WorldCupGame.objects.get(pk=3).date
    if(now > world_cup_start):
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'
        return Response(
                {'errors': {nfe: "Can not use your wildcard now. Second Round of the Group Phase has started"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        user = request.user
        if request.data['wildcard']:
            winner_id = request.data['wildcard']
            user.winner_choice = Team.objects.get(pk=winner_id)
            user.save()
        return Response(status=status.HTTP_201_CREATED)

@api_view(http_method_names=['POST'])
@permission_classes([permissions.IsAuthenticated])
def guess_game_result(request):
    now = timezone.now()
    game_id = request.data['game_id']
    game = WorldCupGame.objects.get(pk=game_id)
    if now > game.date:
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'
        return Response(
                {'errors': {nfe: "Can not update your guess now. Game has already started"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        user = request.user
        choice = request.data['choice']
        try:
            vote = Vote.objects.filter(user=user, game=game)[0]
            vote.choice = choice
            vote.save()
        except:
            Vote.objects.create(user=user, game=game, choice=choice)

        return Response(status=status.HTTP_201_CREATED)

@api_view(http_method_names=['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow(request):
    try:
        current_user = request.user
        followed_user = User.objects.get(pk=request.data['user_id'])
        current_user.following.add(followed_user)
        current_user.save()
        return Response(status=status.HTTP_201_CREATED)
    except:
        return Response(
                {'errors': "No user found with the provided id"},
                status=status.HTTP_400_BAD_REQUEST,
        )

@api_view(http_method_names=['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow(request):
    try:
        current_user = request.user
        unfollowed_user = User.objects.get(pk=request.data['user_id'])
        current_user.following.remove(unfollowed_user)
        current_user.save()
        return Response(status=status.HTTP_201_CREATED)
    except:
        return Response(
                {'errors': "No user found with the provided id"},
                status=status.HTTP_400_BAD_REQUEST,
        )

@api_view(http_method_names=['POST'])
@permission_classes([permissions.IsAuthenticated])
def reset_custom_leaderboard(request):
    request.user.following.clear()
    return Response(status=status.HTTP_201_CREATED)

class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=False).order_by('-score', 'first_name', 'last_name')
    serializer_class = LeaderboardSerializer
    permission_classes = (permissions.IsAuthenticated, )
    http_method_names = ['get']

class MyCustomLeaderboardViewSet(viewsets.ModelViewSet):
    serializer_class = LeaderboardSerializer
    permission_classes = (permissions.IsAuthenticated, )
    http_method_names = ['get']
    def get_queryset(self):
        return self.request.user.following.all()

class TrendViewSet(viewsets.ModelViewSet):
    queryset = WorldCupGame.objects.all()
    serializer_class = TrendSerializer
    permission_classes = (permissions.IsAuthenticated, )
    http_method_names = ['get']

@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    """
    Exchange an OAuth2 access token for one for this site.
    This simply defers the entire OAuth2 process to the front end.
    The front end becomes responsible for handling the entirety of the
    OAuth2 process; we just step in at the end and use the access token
    to populate some user identity.
    The URL at which this view lives must include a backend field, like:
        url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
    Using that example, you could call this endpoint using i.e.
        POST API_ROOT + 'social/facebook/'
        POST API_ROOT + 'social/google-oauth2/'
    Note that those endpoint examples are verbatim according to the
    PSA backends which we configured in settings.py. If you wish to enable
    other social authentication backends, they'll get their own endpoints
    automatically according to PSA.
    ## Request format
    Requests must include the following field
    - `access_token`: The OAuth2 access token provided by the provider
    """
    try:
        serializer = SocialSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # set up non-field errors key
            # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views

            try:
                # this line, plus the psa decorator above, are all that's necessary to
                # get and populate a user object for any properly enabled/configured backend
                # which python-social-auth can handle.
                user = request.backend.do_auth(serializer.validated_data['access_token'])
            except HTTPError as e:
                # An HTTPError bubbled up from the request to the social auth provider.
                # This happens, at least in Google's case, every time you send a malformed
                # or incorrect access key.
                return Response(
                    {'errors': {
                        'token': 'Invalid token',
                        'detail': str(e),
                    }},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if user:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key})
                else:
                    # user is not active; at some point they deleted their account,
                    # or were banned by a superuser. They can't just log in with their
                    # normal credentials anymore, so they can't log in with social
                    # credentials either.
                    return Response(
                        {'errors': {'This user account is inactive'}},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                # Unfortunately, PSA swallows any information the backend provider
                # generated as to why specifically the authentication failed;
                # this makes it tough to debug except by examining the server logs.
                return Response(
                    {'errors': {"Authentication Failed"}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as e:
        return Response(
            {
                'errors': "Authentication Failed",
                "details": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class Logout(APIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({'data': 'logged out'}, status=status.HTTP_200_OK)

def make_prediction(game):
    previous_games = [historical_game.to_dict() for historical_game in HistoricalGame.objects.all()] + [worldcup_game.to_dict() for worldcup_game in WorldCupGame.objects.exclude(home_score__isnull=True)]
    history = pd.DataFrame.from_records(previous_games)
    defense = get_defense_capabilities(history)
    if game.round in [str(group) for group in Group.objects.all()]:
       game_prediction = predict_group_match(str(game.home_team), str(game.away_team),history,defense)
       paul_prediction = Prediction.objects.create(
         game_id=game.id,
         home_win=game_prediction['win'],
         away_win=game_prediction['lose'],
         draw=game_prediction['draw']
       )
    else:
        home_win = win_knockout_match(str(game.home_team), str(game.away_team), history, defense)
        paul_prediction = Prediction.objects.create(
          game_id=game.id,
          home_win=home_win,
          away_win=(1-home_win),
          draw=0
        )
    paul = User.objects.get(email='paul.prediction@wizeline.com')
    paul_vote, created = Vote.objects.get_or_create(user=paul, game=game)
     #Comment this three lines if it is the first time you are running the project in order to let the migrations run ok
    paul_choice = get_paul_choice(paul_prediction.home_win, paul_prediction.away_win, paul_prediction.draw)
    paul_vote.choice = paul_choice
    paul_vote.save()

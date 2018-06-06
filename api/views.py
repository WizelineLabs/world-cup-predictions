from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.models import HistoricalGame, Team, Group, WorldCupGame, Prediction, Vote, User
#from snippets.permissions import IsOwnerOrReadOnly
from api.serializers import HistoricalGameSerializer, TeamSerializer, GroupSerializer, WorldCupGameSerializer, PredictionSerializer, VoteSerializer, UserSerializer

class HistoricalGameViewSet(viewsets.ModelViewSet):
    queryset = HistoricalGame.objects.all()
    serializer_class = HistoricalGameSerializer
    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsOwnerOrReadOnly, )

    # @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
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
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    http_method_names = ['get']

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    http_method_names = ['get', 'post', 'put']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

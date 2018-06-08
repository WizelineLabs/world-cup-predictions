from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from django.urls import path

from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'game', views.WorldCupGameViewSet)
router.register(r'team', views.TeamViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'user', views.UserViewSet, 'user')
router.register(r'prediction', views.PredictionViewSet)
router.register(r'vote', views.VoteViewSet, 'votes')
router.register(r'leaderboard', views.LeaderboardViewSet)
router.register(r'topcontenders', views.TopContendersViewSet)
# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^social/(?P<backend>[^/]+)/$', views.exchange_token, name='google_login'),
    url(r'^wildcard/', views.choose_winner, name='choose_wildcard'),
    url(r'^logout/', views.Logout.as_view()),
]
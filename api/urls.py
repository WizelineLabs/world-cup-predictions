from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
#router.register(r'login', views.login)
router.register(r'game', views.WorldCupGameViewSet)
router.register(r'team', views.TeamViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'prediction', views.PredictionViewSet)
router.register(r'vote', views.VoteViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls))
]
from django.contrib import admin

# Register your models here.

from .models import Team, HistoricalGame, WorldCupGame, User, Vote, Prediction

admin.site.register(Team)
admin.site.register(HistoricalGame)
admin.site.register(WorldCupGame)
admin.site.register(User)
admin.site.register(Vote)
admin.site.register(Prediction)
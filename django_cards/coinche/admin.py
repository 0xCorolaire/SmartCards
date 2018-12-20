from django.contrib import admin

from .models import ListCards, Rules, Bet, TeamOpponent, TeamPersonnal, GameLog

admin.site.register(ListCards)
admin.site.register(Rules)
admin.site.register(Bet)
admin.site.register(GameLog)
admin.site.register(TeamOpponent)
admin.site.register(TeamPersonnal)

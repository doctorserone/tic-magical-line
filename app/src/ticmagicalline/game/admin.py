from django.contrib import admin
import pretty_errors
from game.models import Game, GameMovement

admin.site.register(Game)
admin.site.register(GameMovement)

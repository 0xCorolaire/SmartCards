from django.contrib import auth
from rest_framework import serializers
from models import GameLog, Bet, TeamOpponent, TeamPersonnal


USER_MODEL = auth.get_user_model()


class UserSerializer:
    @classmethod
    def get_user_as_dict(cls, user):
        if user is None:
            return dict(id=None, first_name=None, last_name=None, username=None, email=None)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
        }
    @classmethod
    def get_info_from_user(cls, user, fields):
        user_as_dict = cls.get_user_as_dict(user)
        return { attr: user_as_dict[attr] for attr in fields }

class GameLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameLog
        fields = '__all__'

class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = '__all__'

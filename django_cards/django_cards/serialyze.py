from django.contrib import auth
from rest_framework import serializers
from models import User

class UserSerializer:
    @classmethod
    def get_user_as_dict(cls, user):
        if user is None:
            return dict(username=None, elo=None, credit=None, total_played=None, total_win=None, total_lost=None)
        return {
            'username':user.username,
            'elo': user.elo,
            'credit': user.credit,
            'total_played': user.total_played,
            'total_win': user.total_win,
            'total_lost': user.total_lost
        }
    @classmethod
    def get_info_from_user(cls, user, fields):
        user_as_dict = cls.get_user_as_dict(user)
        return { attr: user_as_dict[attr] for attr in fields }

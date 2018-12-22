# -*- coding: utf-8 -*-

"""
django_cards URL Configuration

C'est ici, dans les URLs de l'application, que toutes les routes sont déclarées.
C'est la variable urlpatterns qui les regroupe, qui est ensuite récupérée par Django
pour en tirer les URLS.

Les URLs sont déclarées :
- individuellement, pour les routes qui effectuent des actions précises

- récupérées par le routeur, pour les routes générées par Django REST Framework. C'est
le include qui est utilisé, et qui récupère auprès du routeur toutes les routes
créées.
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework import routers, serializers, viewsets
from detector import views as detector_views
from coinche import views as coinche_views
from django_cards import views as system_view
# Serializers define the API representation.

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


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^getAiNormalMove$', coinche_views.getAiNormalMove),
    url(r'^getAiRandomMove$', coinche_views.getAiRandomMove),
    url(r'^canPlay$', coinche_views.canPlay),
    url(r'^evaluateFold$', coinche_views.evaluateFold),
    url(r'^getAiBet$', coinche_views.getAiBet),
    url(r'^getRules$', coinche_views.getRules),
    url(r'^getListCards$', coinche_views.getListCards),
    url(r'^getCard$', coinche_views.getCard),
    url(r'^getGameHands$', coinche_views.getGameHands),
    url(r'^sendResultGame$', coinche_views.sendResultGame),
    url(r'^getHandInPhoto$', detector_views.getHandInPhoto),
    url(r'^getCardsInPhoto$', detector_views.getCardsInPhoto),
    url(r'^connexion$', system_view.connexion_api),
    url(r'^register$', system_view.register_api),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

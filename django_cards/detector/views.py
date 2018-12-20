# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework import mixins, viewsets, views
from rest_framework.decorators import (api_view, permission_classes,
                                       renderer_classes)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import json
from coinche import models as coinche_models

"""
Note globale pour ce fichier :

Dans ce fichier, en dehors des viewsets, les vues
simples sont déclarées de deux façons :
- de façon générique Django, avec une fonction qui va se terminer par le retour d'un
render d'une template Django.
- de façon Django REST Framework - cette façon permet de définir clairement les méthodes
HTTP par lesquelles une vue peut être atteinte, et permet de prédéfinir le Content-Type
dans lequel la réponse sera rendue.
Par exemple, pour les vues qui sont sensées retourner du JSON, on utilisera le
renderer REST Framework appelé JSONRenderer.

Ces deux vues peuvent être distinguées par l'utilisation des décorateurs api_view (définition
des méthodes HTTP) et renderer_class (content type du retour), qui sont caractéristiques de
la vue REST Framework.

L'intérêt d'une vue générique Django est de permettre de render une vue, tandis que celle
de la vue Django REST Framework est de pouvoir retourner facilement dans un format voulu.
On utilisera donc principalement les vues traditionnelles pour afficher des pages, et des
vues REST Framework pour des appels d'API (qui serviront, par exemple, en appel AJAX).
user = authenticate(username=username, password=password)
assert isinstance(user, mongoengine.django.auth.User)
"""



@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def getCardsInPhoto(request):
    """
    Endpoint qui permet d'obtenir les cartes présentes sur la photo et retourne une photo avec le nombre de points dans la main
    """
    body = json.loads(request.body)
    photo = body['photo']
    # On envoie la photo dans YOLO et on choppe le retour
    # Une fois la photo retour avec la liste des cartes, on retourne la liste des cartes
    list_cards = []
    final_list_cards = list(set(l))
    total_points = 0
    for e in final_list_cards:
        card = coinche_models.ListCards.objects.filter(
                card_name = e
            ).values('card_name','value_non_atout','value_atout')
        total_point+=card['value_non_atout']

    return Response({
        'list_cartes': final_list_cards,
        'total_point': total_point
    })

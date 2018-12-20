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
from djongo import models
from .models import (ListCards, Rules, GameLog, TeamOpponent, TeamPersonnal, Bet)
from django.core import serializers
from django.forms.models import model_to_dict
import random

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

"""

models.DjongoManager()

class ListCardsView(models.DjongoManager):
    def get_Card(name, queryset=None):
        card = [i for i in ListCards.objects.mongo_aggregate([
            {
                '$match': {
                    'card_name': name
                }
            },
        ])]
        return card

    def get_ListCards(name, queryset=None):
        cards = ListCards.objects.all()
        return cards



"""
API Coinche
"""

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def sendResultGame(request):
    """
    Endpoint qui permet de save les log d'une manche
    On a dans la request :
      Pour la table GameLog
        - team_personnal : un JSON avec
            player_south : le nom du joueur
            south_hand : sa liste de carte tq : 'carte1-carte2-...'
            player_north : partenaire du joueur
            north_hand : la main du partenaire
            south_is_announcing_first : si le joueur a annoncé en premier
            north_is_announcing_first : meme chose
        - team_opponent : Un JSON comme pour la team personnal
        - final_bettor : l'annonceur final !
        - points_done : Le nombre de points effectué !
        - has_won : 0 ou 1 si le joueur a perdu ou gagné !
      Pour la table Bet, chacune des annonces :
        - bettor : le parieur
        - type_bet : type de l'annonce ( TA, couleur..)
        - value_bet : Valeur de l'annonce
        - order_of_bet : l'ordre du bet
        - game_id : l'id de la game
        Ex :
        request :
        {	"has_won" : "1",
        	"points_done" : "160",
        	"final_bettor" : "South",
        	"team_personnal" : {
        		"player_south" : "Player",
        		"south_hand" : "Js-9s-As-8c-Kc-Qd-9d-7d",
        		"player_north" : "Bot",
        		"north_hand" : "7s-Qs-Ah-9h-7h-Jd-Jc-Qc",
        		"south_is_announcing_first" : "1",
        		"north_is_announcing_first" : "0"
        	},
        	"team_opponent" : {
        		"player_south" : "Bot",
        		"south_hand" : "Js-9s-As-8c-Kc-Qd-9d-7d",
        		"player_north" : "Bot",
        		"north_hand" : "7s-Qs-Ah-9h-7h-Jd-Jc-Qc",
        		"south_is_announcing_first" : "0",
        		"north_is_announcing_first" : "0"
        	},
        	"list_bet" : [
        		{
        			"bettor" : "South",
        			"type_bet" : "D",
        			"value_bet" : "80",
        			"order_of_bet" : "1"
        		},
        		{
        			"bettor" : "North",
        			"type_bet" : "D",
        			"value_bet" : "90",
        			"order_of_bet" : "3"
        		}
        	]
        }
    """
    body = json.loads(request.body)
    has_won_i = body['has_won']
    points_done_i = body['points_done']
    final_bettor_i = body['final_bettor']
    team_personnal_i = body['team_personnal']
    team_opponent_i = body['team_opponent']
    game_log_instance = GameLog.objects.create(
        final_bettor=final_bettor_i,
        points_done=points_done_i,
        has_won=has_won_i
    )
    # On récupere le log crée
    id_added_game = GameLog.objects.all()[GameLog.objects.count()-1]
    team_personnal_instance = TeamPersonnal.objects.create(
        player_south=team_personnal_i['player_south'],
        south_hand=team_personnal_i['south_hand'],
        player_north=team_personnal_i['player_north'],
        north_hand=team_personnal_i['north_hand'],
        south_is_announcing_first=team_personnal_i['south_is_announcing_first'],
        north_is_announcing_first=team_personnal_i['north_is_announcing_first'],
        game_id=id_added_game
    )
    team_opponent_instance = TeamOpponent.objects.create(
        player_east=team_opponent_i['player_east'],
        east_hand=team_opponent_i['east_hand'],
        player_west=team_opponent_i['player_west'],
        west_hand=team_opponent_i['west_hand'],
        east_is_announcing_first=team_opponent_i['east_is_announcing_first'],
        west_is_announcing_first=team_opponent_i['west_is_announcing_first'],
        game_id=id_added_game
    )
    #On insere les bets en bulk
    list_bet = body['list_bet']
    bets = [
        Bet(
            bettor=e['bettor'],
            type_bet=e['type_bet'],
            value_bet=e['value_bet'],
            order_of_bet=e['order_of_bet'],
            game_id=id_added_game,
        )
        for e in list_bet
    ]
    bets_instances = Bet.objects.bulk_create(bets)
    return Response(True)

@api_view(['GET'])
@renderer_classes((JSONRenderer, ))
def getRules(request):
    """
    Endpoint qui permet d'avoir les regles possibles de la coinches ( TA, SA , Couleur et nb de pts en tout)
    """
    rules =Rules.objects.all().values('type_announce','total_point')
    return Response(rules)


@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def getGameHands(request):
    """
    Endpoint qui permet d'optenir 4 liste avec distribution aléatoire de 8 cartes par liste
    request : firstGame(true/false), listLastGameCards([
    {
        "card_name": "7s",
        "value_non_atout": 0,
        "value_atout": 0
    },
    ...])
    """
    body = json.loads(request.body)
    firstGame = body['firstGame']
    if firstGame == 'True':
        cards = list(ListCards.objects.all().values('card_name','value_non_atout','value_atout'))
        random.shuffle(cards)
    else:
        lastGameCards = body['listLastGameCards']
        val = random.randint(10,len(lastGameCards)-10)
        cards = lastGameCards[val:]
        del lastGameCards[val:]
        cards.extend(lastGameCards)
    EastHand=[]
    NorthHand=[]
    WestHand=[]
    SouthHand=[]
    for e1 in  range(0,3):
        extract = cards.pop()
        EastHand.append(extract)
    for n1 in  range(0,3):
        extract = cards.pop()
        NorthHand.append(extract)
    for w1 in  range(0,3):
        extract = cards.pop()
        WestHand.append(extract)
    for s1 in  range(0,3):
        extract = cards.pop()
        SouthHand.append(extract)
    for e2 in  range(0,2):
        extract = cards.pop()
        EastHand.append(extract)
    for n2 in  range(0,2):
        extract = cards.pop()
        NorthHand.append(extract)
    for w2 in  range(0,2):
        extract = cards.pop()
        WestHand.append(extract)
    for s2 in  range(0,2):
        extract = cards.pop()
        SouthHand.append(extract)
    for e3 in  range(0,3):
        extract = cards.pop()
        EastHand.append(extract)
    for n3 in  range(0,3):
        extract = cards.pop()
        NorthHand.append(extract)
    for w3 in  range(0,3):
        extract = cards.pop()
        WestHand.append(extract)
    for s3 in  range(0,3):
        extract = cards.pop()
        SouthHand.append(extract)

    return Response({
        'East':EastHand,
        'North':NorthHand,
        'West':WestHand,
        'South':SouthHand
    })

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def ia_bet(request):
    """
    IA d'une annonce simple à la coinche , en request on nous passe la liste de cartes et les anciennes annonces
    """
    body = json.loads(request.body)
    hand = body['player_hand']
    type_card = ['s','c','d','h']
    #On prends la plus longue longe de la main





    return Response()


@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def getCard(request):
    """
    Endpoint qui permet d'avoir une seule carte avec sa valeur
    """
    body = json.loads(request.body)
    name = body['name']
    card = ListCards.objects.filter(
            card_name = name
        ).values('card_name','value_non_atout','value_atout')
    return Response(card)

@api_view(['GET'])
@renderer_classes((JSONRenderer, ))
def getListCards(request):
    """
    Endo=point qui permet d'avoir la liste totale de la coinche avec ses valeurs
    """
    cards =ListCards.objects.all().values('card_name','value_non_atout','value_atout')

    return Response(cards)

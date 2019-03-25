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
from random import randint
from django.views.decorators.csrf import ensure_csrf_cookie

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



Your example sounds similar to Bridge. Top Bridge-playing systems use Monte Carlo methods to select moves. At a high level:

Determine the probabilities of each card being in a given hand. You know with certainty which cards are in your hand and which cards have been played. Determine the probability of all other cards based on cards that have been played and possibly a player's bid if there's bidding involved. To start, you could just use a naive and equal probability that a card is in some player's hand.
Now, run through as many "virtual" games as you can. Simulate playing a card from your hand and then determine your opponents' responses using the rules of the game and your probabilities. For each virtual game, use your probabilities to assign cards to a player and then quickly simulate the game. Assume each player will play to the best of their ability. You know all the cards in your virtual game so you can make each player play perfectly.
When you have a solid sampling (or you run out of time), pick the legal move that gave you the best outcome most often.
Once you get something working, you can add all sorts of enriched strategies. For instance, vary your probabilities based on a player's historic plays, vary probabilities based on a player's style (passive, cautious, aggressive), or even consider the effects of specific players playing together
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
Fonction utiles
"""

def canPlayList(body):
    cards_played = body['cards_played']
    remaining_cards = body['remaining_cards']
    opening_color = body['opening_color']
    atout = body['atout']
    can_play = []
    cards_atout = []
    order_no_a = ['7','8','9','J','Q','K','10','A']
    order_a = ['7','8','Q','K','10','A','9','J']
    if cards_played:
        if opening_color == atout:
            for x in remaining_cards:
                if opening_color in x['card_name']:
                    cards_atout.append(x)
            if not cards_atout:
                can_play=remaining_cards
            else:
                max=0
                if len(cards_played)==1:
                    max=order_a.index(cards_played[0]['idc'])
                    for e in cards_atout:
                        if order_a.index(e['idc']) > max:
                            can_play.append(e)
                    if not can_play:
                        can_play=cards_atout
                elif len(cards_played)==2:
                    max = order_a.index(cards_played[0]['idc'])
                    if atout in cards_played[1]['card_name']:
                        if order_a.index(cards_played[1]['idc']) > max :
                            max = order_a.index(cards_played[1]['idc'])
                            for e in cards_atout:
                                if order_a.index(e['idc']) > max:
                                    can_play.append(e)
                            if not can_play:
                                can_play=cards_atout
                        else:
                            for e in cards_atout:
                                if order_a.index(e['idc']) > max:
                                    can_play.append(e)
                            if not can_play:
                                can_play=cards_atout
                    else:
                        for e in cards_atout:
                            if order_a.index(e['idc']) > max:
                                can_play.append(e)
                        if not can_play:
                            can_play=cards_atout
                else:
                    max = order_a.index(cards_played[0]['idc'])
                    if atout in cards_played[1]['card_name']:
                        if order_a.index(cards_played[1]['idc']) > max :
                            max = order_a.index(cards_played[1]['idc'])
                            if atout in cards_played[2]['card_name']:
                                if order_a.index(cards_played[2]['idc']) > max :
                                    max = order_a.index(cards_played[2]['idc'])
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                                else:
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                            else:
                                for e in cards_atout:
                                    if order_a.index(e['idc']) > max:
                                        can_play.append(e)
                                if not can_play:
                                    can_play=cards_atout
                        else:
                            if atout in cards_played[2]['card_name']:
                                if order_a.index(cards_played[2]['idc']) > max :
                                    max = order_a.index(cards_played[2]['idc'])
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                                else:
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                            else:
                                for e in cards_atout:
                                    if order_a.index(e['idc']) > max:
                                        can_play.append(e)
                                if not can_play:
                                    can_play=cards_atout
                    else:
                        if atout in cards_played[2]['card_name']:
                            if order_a.index(cards_played[2]['idc']) > max :
                                max = order_a.index(cards_played[2]['idc'])
                                for e in cards_atout:
                                    if order_a.index(e['idc']) > max:
                                        can_play.append(e)
                                if not can_play:
                                    can_play=cards_atout
                            else:
                                for e in cards_atout:
                                    if order_a.index(e['idc']) > max:
                                        can_play.append(e)
                                if not can_play:
                                    can_play=cards_atout
                        else:
                            for e in cards_atout:
                                if order_a.index(e['idc']) > max:
                                    can_play.append(e)
                            if not can_play:
                                can_play=cards_atout
        else:
            for x in remaining_cards:
                if opening_color in x['card_name']:
                    can_play.append(x)
            if not can_play:
                i=0
                for x in remaining_cards:
                    if atout in x['card_name']:
                        i+=1
                        cards_atout.append(x)
                if i==0:
                    can_play=remaining_cards
                else:
                    # Le joueur possede un atout, il faut regarder qui est maître
                    if len(cards_played)==3:
                        max=0
                        if atout in cards_played[1]['card_name']:
                            max = order_a.index(cards_played[1]['idc'])
                            if atout in cards_played[2]['card_name']:
                                if order_a.index(cards_played[2]['idc']) > max :
                                    max = order_a.index(cards_played[2]['idc'])
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                                else:
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                            else:
                                can_play=remaining_cards
                        else:
                            if atout in cards_played[2]['card_name']:
                                max = order_a.index(cards_played[2]['idc'])
                                for e in cards_atout:
                                    if order_a.index(e['idc']) > max:
                                        can_play.append(e)
                                if not can_play:
                                    can_play=cards_atout
                            else:
                                if order_no_a.index(cards_played[2]['idc'])<order_no_a.index(cards_played[1]['idc']) and order_no_a.index(cards_played[1]['idc']) >order_no_a.index(cards_played[0]['idc']):
                                    can_play=remaining_cards
                                else:
                                    can_play=cards_atout
                    elif len(cards_played)==1:
                        can_play=cards_atout
                    else:
                        max=0
                        if atout in cards_played[1]['card_name']:
                            max = order_a.index(cards_played[1]['idc'])
                            for e in cards_atout:
                                if order_a.index(e['idc']) > max:
                                    can_play.append(e)
                            if not can_play:
                                can_play=cards_atout
                        else:
                            if order_no_a.index(cards_played[1]['idc'])<order_no_a.index(cards_played[0]['idc']):
                                can_play=remaining_cards
                            else:
                                can_play=cards_atout
    else:
        can_play=remaining_cards
    return can_play


def canBet(body):

    return []

def isWinning(card,cards_played,atout):
    order_no_a = ['7','8','9','J','Q','K','10','A']
    order_a = ['7','8','Q','K','10','A','9','J']
    winning = 0
    if cards_played:
        #Si on joue à l'atout
        if cards_played[0]['idc'] == atout:
            if cards_played[0]['idc'] in card['card_name']:
                max=0
                if len(cards_played)==1:
                    max=order_a.index(cards_played[0]['idc'])
                    if order_a.index(card['idc']) > max:
                        winning=1
                    else:
                        winning=-1
                elif len(cards_played)==2:
                    max = order_a.index(cards_played[0]['idc'])
                    if atout in cards_played[1]['card_name']:
                        if order_a.index(cards_played[1]['idc']) > max :
                            max = order_a.index(cards_played[1]['idc'])
                            if order_a.index(card['idc']) > max:
                                winning=1
                            else:
                                winning=-1
                        else:
                            winning=1
                    else:
                        winning=1
                else:
                    max = order_a.index(cards_played[0]['idc'])
                    if atout in cards_played[1]['card_name']:
                        if order_a.index(cards_played[1]['idc']) > max :
                            max = order_a.index(cards_played[1]['idc'])
                            if atout in cards_played[2]['card_name']:
                                if order_a.index(cards_played[2]['idc']) > max :
                                    max = order_a.index(cards_played[2]['idc'])
                                    if order_a.index(card['idc']) > max:
                                        winning=1
                                    else:
                                        winning=-1
                            else:
                                winning=1
                        else:
                            if atout in cards_played[2]['card_name']:
                                if order_a.index(cards_played[2]['idc']) > max :
                                    max = order_a.index(cards_played[2]['idc'])
                                    if order_a.index(card['idc']) > max:
                                        winning=1
                                    else:
                                        winning=-1
                            else:
                                if order_a.index(card['idc']) > max:
                                    winning=1
                                else:
                                    winning=-1
                    else:
                        if atout in cards_played[2]['card_name']:
                            if order_a.index(cards_played[2]['idc']) > max :
                                max = order_a.index(cards_played[2]['idc'])
                                if order_a.index(card['idc']) > max:
                                    winning=1
                                else:
                                    winning=-1
                        else:
                            if order_a.index(card['idc']) > max:
                                winning=1
                            else:
                                winning=-1
            else:
                winning=-1
        # on ne joue pas à l'atout
        else:
            if len(cards_played)==3:
                max=0
                if atout in cards_played[1]['card_name']:
                    max = order_a.index(cards_played[1]['idc'])
                    if atout in cards_played[2]['card_name']:
                        if order_a.index(cards_played[2]['idc']) > max :
                            max = order_a.index(cards_played[2]['idc'])
                            if atout in card['card_name']:
                                if order_a.index(card['idc']) > max:
                                    winning=1
                                else:
                                    winning=-1
                            else:
                                winning=-1
                        else:
                            winning=1
                    else:
                        winning=1
                else:
                    if atout in cards_played[2]['card_name']:
                        max = order_a.index(cards_played[2]['idc'])
                        if atout in card['card_name']:
                            if order_a.index(card['idc']) > max:
                                winning=1
                            else:
                                winning=-1
                        else:
                            winning=-1
                    else:
                        if order_no_a.index(cards_played[2]['idc'])<order_no_a.index(cards_played[1]['idc']) and order_no_a.index(cards_played[1]['idc']) >order_no_a.index(cards_played[0]['idc']):
                            winning=1
                        else:
                            if order_no_a.index(cards_played[2]['idc'])<order_no_a.index(card['idc']) and order_no_a.index(card['idc']) >order_no_a.index(cards_played[0]['idc']):
                                winning=1
                            else:
                                winning=-1
            elif len(cards_played)==1:
                if order_no_a.index(cards_played[0]['idc'])<order_no_a.index(card['idc']):
                    winning=1
                else:
                    winning=-1
            else:
                max=0
                if atout in cards_played[1]['card_name']:
                    max = order_a.index(cards_played[1]['idc'])
                    if atout in card['card_name']:
                        if order_a.index(card['idc']) > max:
                            winning=1
                        else:
                            winning=-1
                    else:
                        winning=-1
                else:
                    if order_no_a.index(cards_played[1]['idc'])<order_no_a.index(cards_played[0]['idc']):
                        winning=1
                    else:
                        winning=-1
    else:
        winning=1

    return winning

def DecisionMinMax(cards_played,atout,list_possibilities):
#Décide du meilleur coup à jouer
    valeur=[]
    best_move = []
    move_lost = []
    for x in list_possibilities:
        valeur.append(MinMaxAlgo(x,cards_played,atout))
    i=0
    for e in valeur:
        if e == 1:
            best_move.append(list_possibilities[i])
            i+=1
        else:
            move_lost.append(list_possibilities[i])
            i+=1
    card_to_play = []
    if best_move:
        indiceW = randint(0, len(best_move)-1) if len(best_move)> 1 else 0
        card_to_play.append(best_move[indiceW])
    else:
        card_to_play.append(move_lost[0])
        for x in move_lost:
            if x['value_non_atout']<card_to_play[0]['value_non_atout']:
                card_to_play.pop()
                card_to_play.append(x)

    return card_to_play

def MinMaxAlgo (card,cards_played,atout):
# Calcule la valeur de e pour le joueur J selon que e EstUnEtatMax ou pas
    if isWinning(card,cards_played,atout) == 1:
        return 1
    else:
        if isWinning(card,cards_played,atout):
            return -1

"""
API Coinche
"""

@api_view(['GET'])
@renderer_classes((JSONRenderer, ))
def getRules(request):
    """
    Endpoint qui permet d'avoir les regles possibles de la coinches ( TA, SA , Couleur et nb de pts en tout)
    """
    rules =list(Rules.objects.all().values('type_announce','total_point'))
    return Response(rules)

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def getMetaDataGame(request):
    """
    Endpoint qui permet de servir les meta datas de base
    """
    body = json.loads(request.body)
    meta = {}
    meta["id"] = "1"
    meta["name"] = "coinche"
    meta["type"] = body["type"]
    meta["points"] = 1501
    return Response(meta)


@api_view(['GET'])
@renderer_classes((JSONRenderer, ))
def getListCards(request):
    """
    Endo=point qui permet d'avoir la liste totale de la coinche avec ses valeurs
    """
    cards =ListCards.objects.all().values('card_name','value_non_atout','value_atout','idc')

    return Response(cards)

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
        ).values('card_name','value_non_atout','value_atout','idc')
    return Response(card)

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def getGameHands(request):
    """
    Endpoint qui permet d'optenir 4 liste avec distribution aléatoire de 8 cartes par liste
    request : newGame(true/false), listLastGameCards([
    {
        "card_name": "7s",
        "value_non_atout": 0,
        "value_atout": 0
    },
    ...])
    """
    body = json.loads(request.body)
    firstGame = body['newGame']
    if firstGame == 'True':
        cards = list(ListCards.objects.all().values('card_name','value_non_atout','value_atout','idc'))
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
        'P1':EastHand,
        'P2':NorthHand,
        'P3':WestHand,
        'P4':SouthHand
    })

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def getAiBet(request):
    """
    IA d'une annonce simple à la coinche , en request on nous passe la liste de cartes et les anciennes annonces. ON a :
    requests : {
        "player_hand" : [{
            "card_name" : "As",
            "value_atout": "11",
            "value_non_atout": "11",
        },
        {

        }
        ...
        ],
        "partner_bet" : {
            "type_bet" : "D",
            "value_bet" : "80"
        },
        "ennemy_bet" : {
            "type_bet" : "D",
            "value_bet" : "80"
        }
    }
    """
    body = json.loads(request.body)
    total_hand = body['hand']
    hand = []
    partner_bet = body['team_bet']
    ennemy_bet = body['opposant_bet']
    for player_hand in total_hand:
        hand.append(player_hand.get('card_name'))
    s = 0
    c = 0
    d = 0
    h = 0
    card_s = ['s']
    card_c = ['c']
    card_d = ['d']
    card_h = ['h']
    card_As = []
    As = 0
    #On prends la plus longue longe de la main
    for x in hand:
        if "s" in x:
            s+=1
            card_s.append(x)
        if "c" in x:
            c+=1
            card_c.append(x)
        if "d" in x:
            d+=1
            card_d.append(x)
        if "h" in x:
            h+=1
            card_h.append(x)
        if "A" in x:
            As+=1
            card_As.append(x)
    longe_n = max(s,c,d,h)
    # on trouv la couleur de la longe
    color = ""
    if (longe_n==(len(card_s)-1)):
        color = "s"
    if (longe_n==(len(card_c)-1)):
        color = "c"
    if (longe_n==(len(card_d)-1)):
        color = "d"
    if (longe_n==(len(card_h)-1)):
        color = "h"

    if partner_bet['value_bet'] != '0' or ennemy_bet['value_bet'] != '0':
        is_announcing_first ='False'
    else:
        is_announcing_first ='True'
    if longe_n < 3:
        # on trouve la type
        if is_announcing_first=='False' and As != 0:
            if partner_bet['value_bet'] > ennemy_bet['value_bet']:
                if partner_bet['type_bet'].lower() in card_As and As<2:
                    bet = {
                        "type_bet" : "Pass",
                        "value_bet" : "0",
                    }
                else:
                    upbet= 10*As + int(partner_bet['value_bet'])
                    bet = {
                        "type_bet" : partner_bet['type_bet'],
                        "value_bet" : str(upbet),
                    }
            else:
                bet = {
                    "type_bet" : "Pass",
                    "value_bet" : "0",
                }
        else:
            bet = {
                "type_bet" : "Pass",
                "value_bet" : "0",
            }
    else:
        #On a une longe de 3 ou plus, on va étudier la longe
        got_j = 0
        got_9 = 0
        got_a = 0
        for x in hand:
            if color in x:
                if 'J' in x:
                    got_j = 20
                if '9' in x:
                    got_9 = 14
                if 'A' in x:
                    got_a = 11
        sum = got_j+got_a+got_9
        if is_announcing_first == 'False':
            if partner_bet['value_bet'] > ennemy_bet['value_bet'] and As != 0:
                    upbet= 10*As + int(partner_bet['value_bet'])
                    bet = {
                        "type_bet" : partner_bet['type_bet'],
                        "value_bet" : str(upbet),
                    }
            else:
                if (int(ennemy_bet['value_bet'])-int(partner_bet['value_bet']))<20 and As>1:
                    upbet= 10 + int(ennemy_bet['value_bet'])
                    bet = {
                        "type_bet" : partner_bet['type_bet'],
                        "value_bet" : str(upbet),
                    }
                else:
                    bet = {
                        "type_bet" : "Pass",
                        "value_bet" : "0",
                    }
        else:
            if longe_n < 5 :
                if sum < 31 :
                    bet = {
                        "type_bet" : "Pass",
                        "value_bet" : "0",
                    }
                else:
                    if sum < 45 :
                        bet = {
                            "type_bet" : color.upper(),
                            "value_bet" : "80",
                        }
                    else:
                        bet = {
                            "type_bet" : color.upper(),
                            "value_bet" : "90",
                        }
            else:
                if sum > 19 and sum < 30 :
                        bet = {
                            "type_bet" : color.upper(),
                            "value_bet" : "90",
                        }
                else :
                        bet = {
                            "type_bet" : color.upper(),
                            "value_bet" : "100",
                        }
    return Response(bet)

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def canPlay(request):
    """
    Endpoint qui retourne la liste des cartes qui peuvent être jouées ( pour le Player )
    rq : {
        "cards_played" : [
            {
                    "card_name": "As",
                    "value_non_atout": 0,
                    "value_atout": 0,
                    "id" : "A"
            },
            {
                    "card_name": "7s",
                    "value_non_atout": 0,
                    "value_atout": 0,
                    "id" : "7"
            },
            {
                    "card_name": "8s",
                    "value_non_atout": 0,
                    "value_atout": 0,
                    "id" : "8"
            }
        ],
        "atout" : "c",
        "opening_color" : "s",
        "remaining_cards": [
            {
                "card_name": "7d",
                "value_non_atout": 0,
                "value_atout": 0,
                "id":"7"
            },
            {
                "card_name": "Kh",
                "value_non_atout": 4,
                "value_atout": 4,
                "id":"K"
            },
            {
                "card_name": "Ks",
                "value_non_atout": 4,
                "value_atout": 4,
                "id":"K"
            },
            {
                "card_name": "Ac",
                "value_non_atout": 11,
                "value_atout": 11,
                "id":"A"
            },
            {
                "card_name": "9c",
                "value_non_atout": 0,
                "value_atout": 14,
                "id":"9"
            }
        ]
    }
    """
    body = json.loads(request.body)
    cards_played = body['cards_played']
    remaining_cards = body['remaining_cards']
    opening_color = body['opening_color']
    atout = body['atout']
    can_play = []
    cards_atout = []
    order_no_a = ['7','8','9','J','Q','K','10','A']
    order_a = ['7','8','Q','K','10','A','9','J']
    if cards_played:
        if opening_color == atout:
            for x in remaining_cards:
                if opening_color in x['card_name']:
                    cards_atout.append(x)
            if not cards_atout:
                can_play=remaining_cards
            else:
                max=0
                if len(cards_played)==1:
                    max=order_a.index(cards_played[0]['idc'])
                    for e in cards_atout:
                        if order_a.index(e['idc']) > max:
                            can_play.append(e)
                    if not can_play:
                        can_play=cards_atout
                elif len(cards_played)==2:
                    max = order_a.index(cards_played[0]['idc'])
                    if atout in cards_played[1]['card_name']:
                        if order_a.index(cards_played[1]['idc']) > max :
                            max = order_a.index(cards_played[1]['idc'])
                            for e in cards_atout:
                                if order_a.index(e['idc']) > max:
                                    can_play.append(e)
                            if not can_play:
                                can_play=cards_atout
                        else:
                            for e in cards_atout:
                                if order_a.index(e['idc']) > max:
                                    can_play.append(e)
                            if not can_play:
                                can_play=cards_atout
                    else:
                        for e in cards_atout:
                            if order_a.index(e['idc']) > max:
                                can_play.append(e)
                        if not can_play:
                            can_play=cards_atout
                else:
                    max = order_a.index(cards_played[0]['idc'])
                    if atout in cards_played[1]['card_name']:
                        if order_a.index(cards_played[1]['idc']) > max :
                            max = order_a.index(cards_played[1]['idc'])
                            if atout in cards_played[2]['card_name']:
                                if order_a.index(cards_played[2]['idc']) > max :
                                    max = order_a.index(cards_played[2]['idc'])
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                                else:
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                            else:
                                for e in cards_atout:
                                    if order_a.index(e['idc']) > max:
                                        can_play.append(e)
                                if not can_play:
                                    can_play=cards_atout
                        else:
                            if atout in cards_played[2]['card_name']:
                                if order_a.index(cards_played[2]['idc']) > max :
                                    max = order_a.index(cards_played[2]['idc'])
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                                else:
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                            else:
                                for e in cards_atout:
                                    if order_a.index(e['idc']) > max:
                                        can_play.append(e)
                                if not can_play:
                                    can_play=cards_atout
                    else:
                        if atout in cards_played[2]['card_name']:
                            if order_a.index(cards_played[2]['idc']) > max :
                                max = order_a.index(cards_played[2]['idc'])
                                for e in cards_atout:
                                    if order_a.index(e['idc']) > max:
                                        can_play.append(e)
                                if not can_play:
                                    can_play=cards_atout
                            else:
                                for e in cards_atout:
                                    if order_a.index(e['idc']) > max:
                                        can_play.append(e)
                                if not can_play:
                                    can_play=cards_atout
                        else:
                            for e in cards_atout:
                                if order_a.index(e['idc']) > max:
                                    can_play.append(e)
                            if not can_play:
                                can_play=cards_atout
        else:
            for x in remaining_cards:
                if opening_color in x['card_name']:
                    can_play.append(x)
            if not can_play:
                i=0
                for x in remaining_cards:
                    if atout in x['card_name']:
                        i+=1
                        cards_atout.append(x)
                if i==0:
                    can_play=remaining_cards
                else:
                    # Le joueur possede un atout, il faut regarder qui est maître
                    if len(cards_played)==3:
                        max=0
                        if atout in cards_played[1]['card_name']:
                            max = order_a.index(cards_played[1]['idc'])
                            if atout in cards_played[2]['card_name']:
                                if order_a.index(cards_played[2]['idc']) > max :
                                    max = order_a.index(cards_played[2]['idc'])
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                                else:
                                    for e in cards_atout:
                                        if order_a.index(e['idc']) > max:
                                            can_play.append(e)
                                    if not can_play:
                                        can_play=cards_atout
                            else:
                                can_play=remaining_cards
                        else:
                            if atout in cards_played[2]['card_name']:
                                max = order_a.index(cards_played[2]['idc'])
                                for e in cards_atout:
                                    if order_a.index(e['idc']) > max:
                                        can_play.append(e)
                                if not can_play:
                                    can_play=cards_atout
                            else:
                                if order_no_a.index(cards_played[2]['idc'])<order_no_a.index(cards_played[1]['idc']) and order_no_a.index(cards_played[1]['idc']) >order_no_a.index(cards_played[0]['idc']):
                                    can_play=remaining_cards
                                else:
                                    can_play=cards_atout
                    elif len(cards_played)==1:
                        can_play=cards_atout
                    else:
                        max=0
                        if atout in cards_played[1]['card_name']:
                            max = order_a.index(cards_played[1]['idc'])
                            for e in cards_atout:
                                if order_a.index(e['idc']) > max:
                                    can_play.append(e)
                            if not can_play:
                                can_play=cards_atout
                        else:
                            if order_no_a.index(cards_played[1]['idc'])<order_no_a.index(cards_played[0]['idc']):
                                can_play=remaining_cards
                            else:
                                can_play=cards_atout
    else:
        can_play=remaining_cards
    return Response(can_play)

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def getAiRandomMove(request):
    """
    Endpoint qui permet d'obtenir un move d'un Ai random (nul)
    ex :
    {
        "cards_played" : [
            {
                    "card_name": "Ks",
                    "value_non_atout": 0,
                    "value_atout": 0,
                    "id": "K"
            },
            {
                    "card_name": "As",
                    "value_non_atout": 0,
                    "value_atout": 0,
                    "id": "A"
            },
            {
                    "card_name": "8s",
                    "value_non_atout": 0,
                    "value_atout": 0,
                    "id": "s"
            }
        ],
        "atout" : "h",
        "opening_color" : "s",
        "remaining_cards": [
            {
                "card_name": "Ah",
                "value_non_atout": 0,
                "value_atout": 0,
                "id": "A"
            },
            {
                "card_name": "8h",
                "value_non_atout": 4,
                "value_atout": 4,
                "id": "8"
            },
            {
                "card_name": "Kd",
                "value_non_atout": 4,
                "value_atout": 4,
                "id": "K"
            },
            {
                "card_name": "Ac",
                "value_non_atout": 11,
                "value_atout": 11,
                "id": "A"
            },
            {
                "card_name": "10s",
                "value_non_atout": 0,
                "value_atout": 14,
                "id": "10"
            }
        ]
    }
    """
    body = json.loads(request.body)
    cards_played = body['cards_played']
    remaining_cards = body['remaining_cards']
    list_possibilities = canPlayList(body)
    indice = randint(0, len(list_possibilities)-1) if len(list_possibilities)> 1 else 0
    card= list_possibilities[indice]

    return Response(card)

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def getAiNormalMove(request):
    """
    Endpoint qui permet d'obtenir un move d'un Ai normal basé sur un algo MinMax avec une heuristique assez satisfaisante
    ex : {
        "cards_played" : [
            {
                    "card_name": "Ks",
                    "value_non_atout": 0,
                    "value_atout": 0,
                    "id": "K"
            },
            {
                    "card_name": "As",
                    "value_non_atout": 0,
                    "value_atout": 0,
                    "id": "A"
            },
            {
                    "card_name": "8h",
                    "value_non_atout": 0,
                    "value_atout": 0,
                    "id": "8"
            }
        ],
        "atout" : "h",
        "opening_color" : "s",
        "remaining_cards": [
            {
                "card_name": "Ad",
                "value_non_atout": 11,
                "value_atout": 11,
                "id": "A"
            },
            {
                "card_name": "8d",
                "value_non_atout": 0,
                "value_atout": 0,
                "id": "8"
            },
            {
                "card_name": "Kd",
                "value_non_atout": 4,
                "value_atout": 4,
                "id": "K"
            },
            {
                "card_name": "Ac",
                "value_non_atout": 11,
                "value_atout": 11,
                "id": "A"
            },
            {
                "card_name": "10c",
                "value_non_atout": 10,
                "value_atout": 10,
                "id": "10"
            }
        ]
    }
    """
    body = json.loads(request.body)
    cards_played = body['cards_played']
    atout=body['atout']
    remaining_cards = body['remaining_cards']
    list_possibilities = canPlayList(body)
    card = DecisionMinMax(cards_played,atout,list_possibilities)

    return Response(card)

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def evaluateFold(request):
    """
    Endpoint qui permet d'évaluer le gagnant d'un pli de 4 cartes dans l'ordre de jeu avec comme request :
    {
        "atout" : "C"
        "cards_in_fold" : [
            {
                "played_by" : "South",
                "card_name" : "J",
                "card_color" : "c",
                "value": "20",
                "is_atout" : "True"
            },{
                "played_by" : "East",
                "card_name" : "9",
                "card_color" : "c",
                "value": "14",
                "is_atout" : "True"
            },{
                "played_by" : "North",
                "card_name" : "7",
                "card_color" : "c",
                "value": "0",
                "is_atout" : "True"
            },{
                "played_by" : "West",
                "card_name" : "8",
                "card_color" : "h",
                "value": "0",
                "is_atout" : "False"
            }
        ]
    }
    """
    order_no_a = ['7','8','9','J','Q','K','10','A']
    order_a = ['7','8','Q','K','10','A','9','J']
    body = json.loads(request.body)
    atout = body['atout']
    cards_in_fold = body['cards_in_fold']
    tab = [cards_in_fold[0],cards_in_fold[1],cards_in_fold[2],cards_in_fold[3]]
    winner = tab[0]
    if atout in tab[0]['card_color']:
        # on joue à l'atout
        if order_a.index(tab[0]['card_name']) < order_a.index(tab[1]['card_name']) and tab[1]['is_atout']=='True':
            winner = tab[1]
            if order_a.index(winner['card_name']) < order_a.index(tab[2]['card_name']) and tab[2]['is_atout']=='True':
                winner = tab[2]
                if order_a.index(winner['card_name']) < order_a.index(tab[3]['card_name']) and tab[3]['is_atout']=='True':
                    winner = tab[3]
            else:
                if order_a.index(winner['card_name']) < order_a.index(tab[3]['card_name']) and tab[3]['is_atout']=='True':
                    winner = tab[3]
        else:
            if order_a.index(winner['card_name']) < order_a.index(tab[2]['card_name']) and tab[2]['is_atout']=='True':
                winner = tab[2]
                if order_a.index(winner['card_name']) < order_a.index(tab[3]['card_name']) and tab[3]['is_atout']=='True':
                    winner = tab[3]
            else:
                if order_a.index(winner['card_name']) < order_a.index(tab[3]['card_name']) and tab[3]['is_atout']=='True':
                    winner = tab[3]
    else:
        if order_no_a.index(tab[0]['card_name']) < order_no_a.index(tab[1]['card_name']) and tab[1]['is_atout']=='False':
            winner = tab [1]
            if order_no_a.index(winner['card_name']) < order_no_a.index(tab[2]['card_name']) and tab[2]['is_atout']=='False':
                winner = tab[2]
                if order_no_a.index(winner['card_name']) < order_no_a.index(tab[3]['card_name']) and tab[3]['is_atout']=='False':
                    winner = tab[3]
                elif tab[3]['is_atout']=='True':
                    winner = tab[3]
            elif tab[2]['is_atout']=='True':
                winner = tab[2]
                # 2 atout
                if order_a.index(winner['card_name']) < order_a.index(tab[3]['card_name']) and tab[3]['is_atout']=='True':
                    winner = tab[3]
        elif tab[1]['is_atout']=='True':
            winner = tab[1]
            # 1 atout
            if order_a.index(winner['card_name']) < order_a.index(tab[2]['card_name']) and tab[2]['is_atout']=='True':
                winner = tab[2]
                # 2 is_atout
                if order_a.index(winner['card_name']) < order_a.index(tab[3]['card_name']) and tab[3]['is_atout']=='True':
                    winner = tab[3]
        else:
            if order_no_a.index(tab[0]['card_name']) < order_no_a.index(tab[2]['card_name']) and tab[2]['is_atout']=='False':
                winner = tab[2]
                if order_no_a.index(winner['card_name']) < order_no_a.index(tab[3]['card_name']) and tab[3]['is_atout']=='False':
                    winner = tab[3]
                elif tab[3]['is_atout']=='True':
                    winner = tab[3]
            elif tab[2]['is_atout']=='True':
                winner = tab[2]
                # 2 atout
                if order_a.index(winner['card_name']) < order_a.index(tab[3]['card_name']) and tab[3]['is_atout']=='True':
                    winner = tab[3]
            else:
                if order_no_a.index(tab[0]['card_name']) < order_a.index(tab[3]['card_name']) and tab[3]['is_atout']=='False':
                    winner = tab[3]
                elif tab[3]['is_atout']=='True':
                    winner = tab[3]

    return Response(winner)

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

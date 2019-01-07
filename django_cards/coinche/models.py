from djongo import models

class ListCards(models.Model):
    card_name = models.CharField(max_length=10, primary_key=True)
    value_atout = models.IntegerField()
    value_non_atout = models.IntegerField()
    idc = models.CharField(max_length=2)
    objects = models.DjongoManager()

class Rules(models.Model):
    type_announce = models.CharField(max_length=30)
    total_point = models.IntegerField()
    objects = models.DjongoManager()

class GameLog(models.Model):
    _id = models.ObjectIdField()
    final_bettor = models.CharField(max_length=50)
    points_done = models.IntegerField()
    has_won = models.IntegerField()
    objects = models.DjongoManager()

"""
Announce : On a le type d'announce,l'ordre dans laquelle elle a été prononcée, quelle partie, et celui qui a parié
"""

class Bet(models.Model):
    _id = models.ObjectIdField()
    bettor = models.CharField(max_length=11)
    type_bet = models.CharField(max_length=11)
    value_bet = models.IntegerField()
    order_of_bet = models.IntegerField()
    game_id = models.ForeignKey(GameLog, on_delete=models.CASCADE)
    objects = models.DjongoManager()


"""
player_south est en fait le joueur
"""

class TeamPersonnal(models.Model):
    player_south = models.CharField(max_length=100)
    south_hand = models.CharField(max_length=100)
    player_north = models.CharField(max_length=100)
    north_hand = models.CharField(max_length=100)
    south_is_announcing_first = models.IntegerField()
    north_is_announcing_first = models.IntegerField()
    game_id = models.ForeignKey(GameLog, on_delete=models.CASCADE)
    objects = models.DjongoManager()

class TeamOpponent(models.Model):
    player_east = models.CharField(max_length=100)
    east_hand = models.CharField(max_length=100)
    player_west = models.CharField(max_length=100)
    west_hand = models.CharField(max_length=100)
    east_is_announcing_first = models.IntegerField()
    west_is_announcing_first = models.IntegerField()
    game_id = models.ForeignKey(GameLog, on_delete=models.CASCADE)
    objects = models.DjongoManager()

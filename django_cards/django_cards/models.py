from djongo import models

class User(models.Model):
    _id = models.ObjectIdField()
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    elo = models.IntegerField()
    credit = models.IntegerField()
    total_played = models.IntegerField()
    total_win = models.IntegerField()
    total_lost = models.IntegerField()
    objects = models.DjongoManager()

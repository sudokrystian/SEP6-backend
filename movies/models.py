from django.db import models
from django.contrib.auth.models import User

class MovieList(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    list_name = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'movie_list'

class Rating(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    rating = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rating'
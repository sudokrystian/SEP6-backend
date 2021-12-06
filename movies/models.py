from django.db import models
from django.contrib.auth.models import User

class MovieList(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    list_name = models.TextField()

class Rating(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
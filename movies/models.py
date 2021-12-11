from django.db import models
from django.contrib.auth.models import User
import datetime

class MovieList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_name = models.TextField()

class MovieInList(models.Model):
    id = models.AutoField(primary_key=True)
    list = models.ForeignKey(MovieList, on_delete=models.CASCADE)
    movie_id = models.IntegerField()

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    rating = models.IntegerField()
    date = models.CharField(max_length=50, default=datetime.datetime.now().isoformat())

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    date = models.CharField(max_length=50, default=datetime.datetime.now().isoformat())
    comment = models.TextField()
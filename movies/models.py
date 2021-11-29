from django.db import models
from django.contrib.auth.models import User


class Directors(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Movies', on_delete=models.CASCADE)
    person = models.ForeignKey('People', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'directors'


class Movies(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    year = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'


class People(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    birth = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class Ratings(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Movies', on_delete=models.CASCADE)
    rating = models.FloatField()
    votes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ratings'

class Rating(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Movies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'rating'


class Stars(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Movies', on_delete=models.CASCADE)
    person = models.ForeignKey('People', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'stars'
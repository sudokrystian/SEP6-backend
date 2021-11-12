# from django.db import models

# # Model for the database entity
# class Movies(models.Model):
#     # Entity fields
#     id = models.IntegerField(primary_key = True)
#     title = models.CharField(max_length=200)
#     year = models.IntegerField()
#     # Name of the table
#     class Meta:
#         db_table = "movies"

# # Model for the database entity
# class People(models.Model):
#     # Entity fields
#     id = models.IntegerField(primary_key = True)
#     name = models.CharField(max_length=200)
#     birth = models.IntegerField()
#     # Name of the table
#     class Meta:
#         db_table = "people"

# # Model for the database entity
# class Directors(models.Model):
#     # Entity fields
#     id = models.IntegerField(primary_key = True)
#     movie_id = models.ForeignKey(Movies, on_delete=models.CASCADE)
#     person_id = models.ForeignKey(People, on_delete=models.CASCADE)
#     # movie_id = models.ManyToManyField(Movies)
#     # person_id = models.ManyToManyField(People)
#     # Name of the table
#     class Meta:
#         db_table = "directors"

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Directors(models.Model):
    id = models.IntegerField(primary_key = True)
    movie = models.ForeignKey('Movies', on_delete=models.CASCADE)
    person = models.ForeignKey('People', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'directors'


class Movies(models.Model):
    id = models.IntegerField(primary_key = True)
    title = models.TextField()
    year = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'movies'


class People(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.TextField()
    birth = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'people'


class Ratings(models.Model):
    id = models.IntegerField(primary_key = True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    rating = models.FloatField()
    votes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ratings'


class Stars(models.Model):
    id = models.IntegerField(primary_key = True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    person = models.ForeignKey(People, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'stars'

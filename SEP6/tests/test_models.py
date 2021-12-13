from django.test import TestCase
from movies.models import MovieList, MovieInList, Rating, Comment
from django.contrib.auth.models import User
import datetime


class RatingTestCase(TestCase):

    username = "example_user"
    email = "example@mail.com"
    password = "test_password"

    movie_id = 617653
    rating = 5

    def setUp(self):
        user = User.objects.create_user(self.username, self.email, self.password)
        Rating.objects.create(
            user=user,
            movie_id=self.movie_id, rating=self.rating,
            date=datetime.datetime.now().isoformat()
        )

    def test_model_creation(self):
        """Animals that can speak are correctly identified"""
        example_rating = Rating.objects.get(
            user=User.objects.get(username=self.username),
            movie_id=self.movie_id, rating=self.rating
        )

        self.assertEqual(example_rating.rating, self.rating)

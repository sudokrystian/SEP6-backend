from django.test import TestCase
from django.test import Client

from movies.models import Rating
from django.contrib.auth.models import User
import datetime

# Database setup test ======================================================================================
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

# Views test ===============================================================================================
class ViewsTestCase(TestCase):
    client = Client()

    # Index ================================================================================================

    def test_index_loads_properly(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # Movies ================================================================================================

    example_movie_id = 617653
    example_movie_name = "spider"

    def test_get_movie_images(self):
        response = self.client.get(
            '/movies/' + str(self.example_movie_id) + "/images")
        self.assertEqual(response.status_code, 200)

    def test_get_movie_crew(self):
        response = self.client.get(
            '/movies/' + str(self.example_movie_id) + "/credits")
        self.assertEqual(response.status_code, 200)

    def test_get_similar_movies(self):
        response = self.client.get(
            '/movies/' + str(self.example_movie_id) + "/similar")
        self.assertEqual(response.status_code, 200)

    def test_get_trending_movies(self):
        response = self.client.get(
            '/movies/trending'
        )
        self.assertEqual(response.status_code, 200)

    def test_get_movies_by_name(self):
        response = self.client.get(
            '/search/movie/page/1/name/' + str(self.example_movie_id))
        self.assertEqual(response.status_code, 200)

    # People ================================================================================================

    example_person_id = 1
    example_person_name = "John"

    def test_get_trending_people(self):
        response = self.client.get('/people/trending')
        self.assertEqual(response.status_code, 200)

    def test_get_person_by_name(self):
        response = self.client.get(
            '/search/people/page/1/name/' + str(self.example_person_name))
        self.assertEqual(response.status_code, 200)

    def test_get_person_credits(self):
        response = self.client.get(
            '/people/' + str(self.example_person_id) + "/credits")
        self.assertEqual(response.status_code, 200)

    # Ratings ==============================================================================================

    def test_get_ratings_for_the_user(self):
        response = self.client.get('/rating/user')
        self.assertEqual(response.status_code, 401)

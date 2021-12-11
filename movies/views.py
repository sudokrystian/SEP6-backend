from django.conf import settings
from django.template import loader
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from movies.models import MovieList, MovieInList, Rating, Comment
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

import requests
import json

# Only for development ===========================
from datetime import timedelta
import datetime
import random
# ================================================

API_KEY = "ea8b367c3b33beb9d31bc05cd0726c57"
API_URL = "https://api.themoviedb.org/3/"

# Main page


def getIndex(request):
    template = loader.get_template('./main/index.html')
    return HttpResponse(template.render())

# Movies ================================================================================================


class TrendingMovies(APIView):
    # Get trending movies
    def get(self, request):
        parameters = {'api_key': API_KEY}
        api_path = "trending/movie/week"
        request = API_URL + api_path
        request_answer = requests.get(url=request, params=parameters)
        if(request_answer.ok):
            return HttpResponse(request_answer, status=status.HTTP_200_OK)
        else:
            return HttpResponse(request_answer, status=404)


class MovieById(APIView):
    # Get movie by id
    def get(self, request, movie_id):
        request_answer = getMovieById(movie_id)
        if(request_answer.ok):
            return HttpResponse(request_answer)
        else:
            return HttpResponse(request_answer, status=404)


class MovieCrew(APIView):
    # Get movie credits (the entire movie crew)
    def get(self, request, movie_id):
        parameters = {'api_key': API_KEY}
        api_path = "movie/" + str(movie_id) + "/credits"
        request = API_URL + api_path
        request_answer = requests.get(url=request, params=parameters)
        if(request_answer.ok):
            return HttpResponse(request_answer)
        else:
            return HttpResponse(request_answer, status=404)


class MovieByName(APIView):
    # Get movie by name
    def get(self, request, page_number, movie_name):
        parameters = {"api_key": API_KEY,
                      "page": page_number, "query": movie_name}
        request = API_URL + "search/movie"
        request_answer = requests.get(request, params=parameters)
        if(request_answer.ok):
            return HttpResponse(request_answer)
        else:
            return HttpResponse(request_answer, status=404)


class MovieImg(APIView):
    # Get movie by name
    def get(self, request, movie_id):
        parameters = {"api_key": API_KEY}
        request = API_URL + "movie/" + str(movie_id) + "/images"
        request_answer = requests.get(request, params=parameters)
        if(request_answer.ok):
            return HttpResponse(request_answer)
        else:
            return HttpResponse(request_answer, status=404)


class MovieSimilar(APIView):
    # Get similiar movies
    def get(self, request, movie_id):
        parameters = {"api_key": API_KEY}
        request = API_URL + "movie/" + str(movie_id) + "/similar"
        request_answer = requests.get(request, params=parameters)
        if(request_answer.ok):
            return HttpResponse(request_answer)
        else:
            return HttpResponse(request_answer, status=404)
# =======================================================================================================

# People ================================================================================================


class PersonById(APIView):
    # Get a person by id
    def get(self, request, person_id):
        parameters = {'api_key': API_KEY}
        api_path = "person/" + str(person_id)
        request = API_URL + api_path
        request_answer = requests.get(url=request, params=parameters)
        if(request_answer.ok):
            return HttpResponse(request_answer)
        else:
            return HttpResponse(request_answer, status=404)

class PersonCredits(APIView):
    # Get person credits (f.e movies that he starred in)
    def get(self, request, person_id):
        parameters = {'api_key': API_KEY}
        api_path = "person/" + str(person_id) + "/movie_credits"
        request = API_URL + api_path
        request_answer = requests.get(url=request, params=parameters)
        if(request_answer.ok):
            return HttpResponse(request_answer)
        else:
            return HttpResponse(request_answer, status=404)

class PeopleByName(APIView):
    # Find people by name
    def get(self, request, page_number, person_name):
        parameters = {"api_key": API_KEY,
                      "page": page_number, "query": person_name}
        request = API_URL + "search/person"
        request_answer = requests.get(request, params=parameters)
        if(request_answer.ok):
            return HttpResponse(request_answer)
        else:
            return HttpResponse(request_answer, status=404)


class TrendingPeople(APIView):
    # Get trending movies
    def get(self, request):
        parameters = {'api_key': API_KEY}
        api_path = "trending/person/week"
        request = API_URL + api_path
        request_answer = requests.get(url=request, params=parameters)
        if(request_answer.ok):
            return HttpResponse(request_answer, status=status.HTTP_200_OK)
        else:
            return HttpResponse(request_answer, status=404)
# =======================================================================================================

# Ratings ==============================================================================================


class AddRating(APIView):
    permission_classes = [IsAuthenticated]
    # Add a new rating
    def put(self, request):
        try:
            json_data = json.loads(request.body)
            user = User.objects.get(pk=request.user.id)
            movie_id = json_data['movie_id']
            rating = json_data['rating']
            # If the user voted for this movie already, return 409
            if(len(Rating.objects.filter(user=user, movie_id=movie_id).values()) != 0):
                return HttpResponse("The user already rated the movie", status=409)
            rating = Rating.objects.create(
                user=user,
                movie_id=movie_id,
                rating=rating,
                date= datetime.datetime.now().isoformat()
            )
            return HttpResponse(status=201)
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {movie_id:'value', rating:'value'}", status=400)
    # Update the current rating of the movie
    def post(self, request):
        try:
            json_data = json.loads(request.body)
            rating_id = json_data['rating_id']
            newRating = json_data['rating']
            rating = get_object_or_404(Rating, pk=rating_id)
            rating.rating = newRating
            rating.date = datetime.datetime.now().isoformat()
            # If the user voted for this movie already, return 409
            rating.save()
            return HttpResponse(rating, status=200)
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {rating_id:'value', rating:'value'}", status=400)


class UserMovieRating(APIView):
    permission_classes = [IsAuthenticated]
    # Get ratings for the movie for the specified user
    def get(self, request, movie_id):
        user = User.objects.get(pk=request.user.id)
        ratings = Rating.objects.filter(
            movie_id=movie_id, user=user).values()
        if(len(ratings) != 0):
            serialized_values = json.dumps(
                list(ratings), cls=DjangoJSONEncoder)
            return HttpResponse(serialized_values, status=200)
        else:
            return HttpResponse("No ratings found", status=404)


class MovieRating(APIView):
    # Get all the ratings for the movie with the specified id
    def get(self, request, movie_id):
        ratings = Rating.objects.filter(movie_id=movie_id).values()
        if(len(ratings) != 0):
            serialized_values = json.dumps(
                list(ratings), cls=DjangoJSONEncoder)
            return HttpResponse(serialized_values, status=200)
        else:
            return HttpResponse("No ratings found", status=404)


class UserRatings(APIView):
    permission_classes = [IsAuthenticated]
    # Get all the ratings given away by the user

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        ratings = Rating.objects.filter(user=user).values()
        if(len(ratings) != 0):
            serialized_values = json.dumps(
                list(ratings), cls=DjangoJSONEncoder)
            return HttpResponse(serialized_values, status=200)
        else:
            return HttpResponse("No ratings found", status=404)
# ======================================================================================================

# Movie lists =========================================================================================


class MovieListsDetails(APIView):
    permission_classes = [IsAuthenticated]
    # Get a movie list with all the details

    def get(self, request):
        lists_by_user = MovieList.objects.filter(user=request.user.id)
        detailed_lists = []
        for list in lists_by_user:
            container = {"list_id": list.id,
                         "list_name": list.list_name, "movies": []}
            movies_in_list = MovieInList.objects.filter(list=list)
            for movie in movies_in_list:
                movie_json = getMovieById(movie.movie_id).json()
                container['movies'].append(movie_json)
            detailed_lists.append(container)
        if(len(detailed_lists) != 0):
            return JsonResponse(detailed_lists, safe=False)
        else:
            return HttpResponse("No movie lists found for the " + str(request.user), status=404)


class MovieLists(APIView):
    permission_classes = [IsAuthenticated]
    # Get movie list for the user

    def get(self, request):
        lists_by_user = MovieList.objects.filter(user=request.user.id).values()
        if(len(lists_by_user) > 0):
            serialized_values = json.dumps(
                list(lists_by_user), cls=DjangoJSONEncoder)
            return HttpResponse(serialized_values)
        else:
            return HttpResponse("No movie lists found for the " + str(request.user), status=404)
    # Create a new movie list

    def put(self, request):
        try:
            json_data = json.loads(request.body)
            list_name = json_data['list_name']
            list = MovieList.objects.create(
                user=User.objects.get(pk=request.user.id),
                list_name=list_name
            )
            return HttpResponse(status=201)
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {list_name:'value'}", status=400)


class MovieListDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, list_id):
        movie_list = get_object_or_404(MovieList, pk=list_id)
        movie_list.delete()
        return HttpResponse(status=200)


class MoviesInList(APIView):
    permission_classes = [IsAuthenticated]
    # Get movies in the list for the user

    def get(self, request, list_id):
        list = MovieList.objects.get(pk=list_id)
        data = serializers.serialize(
            "json", MovieInList.objects.filter(list=list))
        transformed_data = json.loads(data)
        arr = []
        for entry in transformed_data:
            arr.append(entry['fields'])
        if(len(arr) != 0):
            return JsonResponse(arr, safe=False)
        else:
            return HttpResponse("No movie lists found for the " + str(request.user), status=404)


class MovieAddToList(APIView):
    permission_classes = [IsAuthenticated]
    # Add a movie to an existing list

    def put(self, request):
        try:
            json_data = json.loads(request.body)
            list_id = json_data['list_id']
            movie_id = json_data['movie_id']
            list = MovieList.objects.get(pk=list_id)
            movie_in_list = MovieInList.objects.filter(
                list=list,
                movie_id=movie_id
            )
            if(len(movie_in_list) == 0):
                new_movie_in_list = MovieInList.objects.create(
                    list=list,
                    movie_id=movie_id
                )
                return HttpResponse(status=201)
            else:
                return HttpResponse("Movie with id " + str(movie_id) + " already exists in the list " + list.list_name, status=403)
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {movie_id:'value', list_id:'value'}", status=400)


class MovieDeleteFromList(APIView):
    permission_classes = [IsAuthenticated]
    # Remove the movie from the list

    def delete(self, request, list_id, movie_id):
        list = MovieList.objects.get(pk=list_id)
        movie_in_list = get_object_or_404(
            MovieInList, list=list, movie_id=movie_id)
        movie_in_list.delete()
        return HttpResponse(status=201)
# ======================================================================================================

# User =================================================================================================


class RegisterUser(APIView):
    permission_classes = [AllowAny]
    # Register the user

    def put(self, request):
        json_data = json.loads(request.body)
        try:
            username = json_data['username']
            email = json_data['email']
            password = json_data['password']
            if User.objects.filter(username=username).exists():
                existing_user = User.objects.filter(username=username)
                return HttpResponse("User with username " + str(existing_user) + " already exists", status=403)
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                return HttpResponse(status=201)
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {username:'value', email:'value', password:'value'}", status=400)


# Comments =================================================================================================
class Comments(APIView):
    def get(self, request, movie_id):
        comment_list = Comment.objects.filter(movie_id=movie_id)
        all_comments = []
        for comment in comment_list:
            container = {
                "id": comment.id,
                "user": comment.user.username,
                "movie_id": comment.movie_id,
                "date": comment.date,
                "comment": comment.comment
            }
            all_comments.append(container)

        return JsonResponse(all_comments, safe=False)


class CommentAdd(APIView):
    permission_classes = [IsAuthenticated]
    # Add a comment
    def put(self, request):
        json_data = json.loads(request.body)
        try:
            movie_id = json_data['movie_id']
            comment = json_data['comment']
            user = User.objects.get(pk=request.user.id)
            Comment.objects.create(
                user=user, movie_id=movie_id, comment=comment, date=datetime.datetime.now().isoformat())
            return HttpResponse(status=201)

        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {comment:'value'}", status=400)


# Utility =====================================================================================================

def getMovieById(movie_id):
    parameters = {'api_key': API_KEY}
    api_path = "movie/" + str(movie_id)
    newRequest = API_URL + api_path
    request_answer = requests.get(url=newRequest, params=parameters)
    return request_answer


# Development =================================================================================================

def test(request):
    user = User.objects.get(pk=1)
    today = datetime.datetime.now()
    for x in range(20):
        Rating.objects.create(
            user=user,
            movie_id=617653,
            rating=random.randint(1, 9),
            date=today.isoformat()
        )
    yesterday = today - datetime.timedelta(days=1)
    for x in range(10):
        Rating.objects.create(
            user=user,
            movie_id=617653,
            rating=random.randint(1, 9),
            date=yesterday.isoformat()
        )
    one_week_ago = today - datetime.timedelta(days=7)
    for x in range(14):
        Rating.objects.create(
            user=user,
            movie_id=617653,
            rating=random.randint(4, 9),
            date=one_week_ago.isoformat()
        )
    return HttpResponse("ok")

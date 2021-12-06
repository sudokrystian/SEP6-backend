from django.conf import settings
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from movies.models import MovieList, Rating

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

import requests
import json

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
        parameters = {'api_key': API_KEY}
        api_path = "movie/" + str(movie_id)
        request = API_URL + api_path
        request_answer = requests.get(url=request, params=parameters)
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
                rating=rating
            )
            return HttpResponse(rating, status=200)
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {movie_id:'value', rating:'value'}", status=400)
    # Update the current rating of the movie
    def post(self, request):
        try:
            json_data = json.loads(request.body)
            user = User.objects.get(pk=request.user.id)
            rating_id = json_data['rating_id']
            newRating = json_data['rating']
            rating = get_object_or_404(Rating, pk=rating_id)
            rating.rating = newRating
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
            return HttpResponse(ratings, status=200)
        else:
            return HttpResponse("No ratings found", status=404)


class MovieRating(APIView):
    # Get all the ratings for the movie with the specified id
    def get(self, request, movie_id):
        ratings = Rating.objects.filter(movie_id=movie_id).values()
        if(len(ratings) != 0):
            return HttpResponse(ratings, status=200)
        else:
            return HttpResponse("No ratings found", status=404)


class UserRatings(APIView):
    permission_classes = [IsAuthenticated]
    # Get all the ratings given away by the user

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        ratings = Rating.objects.filter(user=user).values()
        if(len(ratings) != 0):
            return HttpResponse(ratings, status=200)
        else:
            return HttpResponse("No ratings found", status=404)
# ======================================================================================================

# Movie lists =========================================================================================


class MovieLists(APIView):
    permission_classes = [IsAuthenticated]
    # Get movie list for the user or create a new movie list
    def get(self, request):
        lists_by_user = MovieList.objects.filter(user=request.user.id).values()
        dictionary = {}
        for list in lists_by_user:
            movie_id = list['movie_id']
            movie = movie_id
            if list['list_name'] not in dictionary:
                dictionary[list['list_name']] = []
            dictionary[list['list_name']].append(model_to_dict(movie))
        if(len(lists_by_user) > 0):
            return HttpResponse(json.dumps(dictionary))
        else:
            return HttpResponse("No movie lists found for the user with an ID " + str(request.user.id), status=404)
    def put(self, request):
        try:
            json_data = json.loads(request.body)
            movie_id = json_data['movie_id']
            list_name = json_data['list_name']
            list = MovieList.objects.create(
                user=User.objects.get(pk=request.user.id),
                movie=movie_id,
                list_name=list_name
            )
            return HttpResponse(list, status=200)
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {movie_id:'value', list_name:'value'}", status=400)
# ======================================================================================================

# User =================================================================================================

class RegisterUser(APIView):
    # Register the user
    def put(self, request):
        json_data = json.loads(request.body)
        try:
            # If json data doesn't exist return autoamtically returns 500
            username = json_data['username']
            email = json_data['email']
            password = json_data['password']
            user = User.objects.create_user(username, email, password)
            # If unique constrains fail server will return 500
            user.save()
            return HttpResponse("User " + username + " registered", status=200)
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {username:'value', email:'value', password:'value'}", status=400)
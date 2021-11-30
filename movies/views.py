from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from collections import defaultdict
from movies.models import Movies, People, Directors, Ratings, MovieList
import json

# Main page

def getIndex(request):
    template = loader.get_template('./main/index.html')
    return HttpResponse(template.render())
    # return HttpResponse("Welcome to the main page")


# Movies ================================================================================================

# Get all movies
def getMovies(request):
    movie_list = list(Movies.objects.all().values())
    return HttpResponse(movie_list)
# Get movie by id
def getMovieById(request, movie_id):
    movie = Movies.objects.filter(id=movie_id).values()
    if len(movie) > 0:
        return HttpResponse(movie)
    else:
        return HttpResponse("No movie with id " + str(movie_id) + " found", status=404)
# Get movie by name
def getMovieByName(request, movie_name):
    movie = Movies.objects.filter(title__contains=movie_name).values()
    if len(movie) > 0:
        return HttpResponse(movie)
    else:
        return HttpResponse("No movie with name " + str(movie_name) + " found", status=404)

# =======================================================================================================

# People ================================================================================================

# Get all people
def getPeople(request):
    people_list = list(People.objects.all().values())
    return HttpResponse(people_list)
# Get person by id
def getPeopleById(request, person_id):
    person = People.objects.filter(id = person_id).values()
    if len(person) > 0:
        return HttpResponse(person)
    else:
        return HttpResponse("No person with id " + str(person) + " found", status=404)


# =======================================================================================================

# Directors # ===========================================================================================

# Get all directors
def getDirectors(request):
    directors_list = list(Directors.objects.all().values())
    return HttpResponse(directors_list)


def getDirectorsByMovieId(request, movie_id):
    directors_by_movie = Directors.objects.filter(movie_id = movie_id).values()
    if len(directors_by_movie) > 0:
        return HttpResponse(directors_by_movie)
    else:
        return HttpResponse("No directors found for the movie with id " + str(movie_id), status=404)


def getDirectorsByPersonId(request, person_id):
    directors_by_person = Directors.objects.filter(person_id=person_id).values()
    if len(directors_by_person) > 0:
        return HttpResponse(directors_by_person)
    else:
        return HttpResponse("No directors found for the person with id " + str(person_id), status=404)


# ======================================================================================================

# Ratings ==============================================================================================

# Get ratings for the movie
def getRatingsByMovie(request, movie_id):
    rating_by_movie = Ratings.objects.filter(movie_id = movie_id).values()
    if(len(rating_by_movie) > 0):
        return HttpResponse(rating_by_movie)
    else:
        return HttpResponse("No rating found for the movie with an ID " + str(movie_id), status=404)      


# ======================================================================================================

# Movie lists =========================================================================================

# Get movie list for the user or create a new movie list
def movieLists(request):
    if request.user.is_authenticated:
        if(request.method == 'GET'):
            lists_by_user = MovieList.objects.filter(user = request.user.id).values()
            # print(lists_by_user)

            dictionary = {}
            for list in lists_by_user:
                movie_id = list['movie_id']
                movie = Movies.objects.get(pk=movie_id)
                if list['list_name'] not in dictionary:
                    dictionary[list['list_name']] = []
                dictionary[list['list_name']].append(model_to_dict(movie))
            if(len(lists_by_user) > 0):
                return HttpResponse(json.dumps(dictionary))
            else:
                return HttpResponse("No movie lists found for the user with an ID " + str(request.user.id), status=404)  
        elif(request.method == 'PUT'):
            try:
                json_data = json.loads(request.body)
                movie_id = json_data['movie_id']
                list_name = json_data['list_name']
                list = MovieList.objects.create(
                    user = User.objects.get(pk=request.user.id), 
                    movie = Movies.objects.get(pk=movie_id), 
                    list_name = list_name
                    )
                return HttpResponse(list, status=200)
            except KeyError:
                return HttpResponse("JSON format is incorrect. Please use {movie_id:'value', list_name:'value'}",status=400)
        else:
            return HttpResponse("Only logged in users have access to this endpoint", status=403)
    else: 
        return HttpResponse("Only logged in users have access to this endpoint", status=403)
        

# ======================================================================================================

# User =================================================================================================

# Register the user
def registerUser(request):
    if request.method == 'PUT':
        json_data = json.loads(request.body)
        try:
            # If json data doesn't exist return autoamtically returns 500
            username = json_data['username']
            email = json_data['email']
            password = json_data['password']
            user = User.objects.create_user(username, email, password)
            # If unique constrains fail server will return 500
            user.save()
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {username:'value', email:'value', password:'value'}",status=400)

        return HttpResponse("User " + username + " registered", status=200)

# Login and become the user
def becomeUser(request):
    if(request.method == 'POST'):
        json_data = json.loads(request.body)
        try:
            username_from_json = json_data['username']
            password_from_json = json_data['password']
            user = authenticate(username = username_from_json, password=password_from_json)
            # if correct
            if user is not None:
                login(request, user)
                return HttpResponse("User logged in", status=200)
            else:
                return HttpResponse("Incorrect login or password", status=401)
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please provide username and password", status=400)

        

# Remove yourself from session == logout
def logout_from_service(request):
    logout(request)
    return HttpResponse("User logged out", status=200)

# Dev endpoint, to be deleted. Returns all users if you are logged in
def getUsers(request):
    if request.user.is_authenticated:
        user_list = list(User.objects.all().values())
        return HttpResponse(user_list)
    else:
        return HttpResponse("Only logged in users have access to this endpoint", status=403)

    

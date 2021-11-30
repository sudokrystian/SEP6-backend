from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from movies.models import MovieList, Rating
import requests
import json

API_KEY = "ea8b367c3b33beb9d31bc05cd0726c57"
API_URL = "https://api.themoviedb.org/3/"

# Main page
def getIndex(request):
    template = loader.get_template('./main/index.html')
    return HttpResponse(template.render())

# Movies ================================================================================================

# Get the movies that are trending this week
def getTrendingMovies(request):
    if(request.method == 'GET'):
        parameters = {'api_key': API_KEY}
        api_path = "trending/movie/week"
        request = API_URL + api_path
        request_answer = requests.get(url = request, params=parameters)
        return HttpResponse(request_answer)
    else:
        return HttpResponse("Endpoint not found", status=404)

# Get movie by id
def getMovieById(request, movie_id):
    if(request.method == 'GET'):
        parameters = {'api_key': API_KEY}
        api_path = "movie/" + str(movie_id)
        request = API_URL + api_path
        request_answer = requests.get(url = request, params=parameters)
        return HttpResponse(request_answer)
    else:
        return HttpResponse("Endpoint not found", status=404)

# Get movie cast
def getMovieCrew(request, movie_id):
    if(request.method == 'GET'):
        parameters = {'api_key': API_KEY}
        api_path = "movie/" + str(movie_id) + "/credits"
        request = API_URL + api_path
        request_answer = requests.get(url = request, params=parameters)
        return HttpResponse(request_answer)
    else:
        return HttpResponse("Endpoint not found", status=404)
# =======================================================================================================

# People ================================================================================================

# Get person by id
def getPersonById(request, person_id):
    if(request.method == 'GET'):
        parameters = {'api_key': API_KEY}
        api_path = "person/" + str(person_id)
        request = API_URL + api_path
        request_answer = requests.get(url = request, params=parameters)
        return HttpResponse(request_answer, status=request_answer.status_code)
    else:
        return HttpResponse("Endpoint not found", status=404)


# =======================================================================================================

# Ratings ==============================================================================================

# Post rating for the movie
def addRating(request):
    if request.user.is_authenticated:
        if(request.method == 'PUT'):
            try:
                json_data = json.loads(request.body)
                user = User.objects.get(pk=request.user.id)
                movie_id = json_data['movie_id']
                rating = json_data['rating']
                # If the user voted for this movie already, return 409
                print(Rating.objects.filter(user = user, movie_id= movie_id).values())
                if(len(Rating.objects.filter(user = user, movie_id= movie_id).values()) != 0):
                    return HttpResponse("The user already rated the movie", status=409)
                rating = Rating.objects.create(
                    user = user, 
                    movie_id = movie_id, 
                    rating = rating
                    )
                return HttpResponse(rating, status=200)
            except KeyError:
                return HttpResponse("JSON format is incorrect. Please use {movie_id:'value', rating:'value'}",status=400)
        else:
            return HttpResponse("Endpoint not found", status=404)
    else:
        return HttpResponse("Only logged in users have access to this endpoint", status=403)

# Get ratings for the movie
def getRatingsByMovie(request, movie_id):
    if(request.method == 'GET'):
        ratings = Rating.objects.filter(movie_id = movie_id).values()
        if(len(ratings) != 0):
            return HttpResponse(ratings, status=200)
        else:
            return HttpResponse("No ratings found", status=404)
    else:
        return HttpResponse("Endpoint not found", status=404)

def getRatingsByUser(request):
    if request.user.is_authenticated:
        if(request.method == 'GET'):
            user = User.objects.get(pk=request.user.id)
            ratings = Rating.objects.filter(user = user).values()
            if(len(ratings) != 0):
                return HttpResponse(ratings, status=200)
            else:
                return HttpResponse("No ratings found", status=404)
        else:
            return HttpResponse("Endpoint not found", status=404)
    else:
        return HttpResponse("Only logged in users have access to this endpoint", status=403)

# Get ratings for the movie for the specified user
def getUserRatingForTheMovie(request, movie_id):
    if request.user.is_authenticated:
        if(request.method == 'GET'):
            user = User.objects.get(pk=request.user.id)
            ratings = Rating.objects.filter(movie_id = movie_id, user = user).values()
            if(len(ratings) != 0):
                return HttpResponse(ratings, status=200)
            else:
                return HttpResponse("No ratings found", status=404)
        else:
            return HttpResponse("Endpoint not found", status=404)
    else:
        return HttpResponse("Only logged in users have access to this endpoint", status=403)

# ======================================================================================================

# Movie lists =========================================================================================

# Get movie list for the user or create a new movie list
def movieLists(request):
    if request.user.is_authenticated:
        if(request.method == 'GET'):
            lists_by_user = MovieList.objects.filter(user = request.user.id).values()
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
        elif(request.method == 'PUT'):
            try:
                json_data = json.loads(request.body)
                movie_id = json_data['movie_id']
                list_name = json_data['list_name']
                list = MovieList.objects.create(
                    user = User.objects.get(pk=request.user.id), 
                    movie = movie_id, 
                    list_name = list_name
                    )
                return HttpResponse(list, status=200)
            except KeyError:
                return HttpResponse("JSON format is incorrect. Please use {movie_id:'value', list_name:'value'}",status=400)
        else:
            return HttpResponse("Endpoint not found", status=404)
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
            return HttpResponse("User " + username + " registered", status=200)
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please use {username:'value', email:'value', password:'value'}",status=400)
    else:
        return HttpResponse("Endpoint not found", status=404)

        

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
    else:
        return HttpResponse("Endpoint not found", status=404)


        

# Remove yourself from session == logout
def logout_from_service(request):
    logout(request)
    return HttpResponse("User logged out", status=200)

    

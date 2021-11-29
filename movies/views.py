from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from movies.models import Movies, People, Directors, Ratings, Rating
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

# def getRating(request):
#     if request.method == 'PUT':
#         json_data = json.loads(request.body)
#         movie_id = json_data['movie_id']
#         rating = json_data['rating']

def getRating(request, movie_id):
    rating_by_movie = Ratings.objects.filter(movie_id = movie_id).values()
    if(len(rating_by_movie) > 0):
        return HttpResponse(rating_by_movie)
    else:
        return HttpResponse("No rating found for the movie with an ID " + str(movie_id))

def getAllRatings(request):
    rating_list = list(Rating.objects.all().values())
    return HttpResponse(rating_list)

def getRating2(request, movie_id):
    rating_by_movie = Rating.objects.filter(movie_id = movie_id).values()
    if(len(rating_by_movie) > 0):
        return HttpResponse(rating_by_movie)
    else:
        return HttpResponse("No rating found for the movie with an ID " + str(movie_id))

def populateRatings(request):
    ratings = Ratings.objects.all().values()
    print(ratings[0]['rating'])
    for rating in ratings:
        amount_of_inputs = int(rating['votes'])
        for x in range(amount_of_inputs):
            rating_obj = Rating()
            rating_obj.movie = Movies.objects.get(pk=rating['movie_id'])
            rating_obj.user = User.objects.get(pk=1)
            rating_obj.rating = rating['rating']
            rating_obj.save()
    return HttpResponse(ratings)
        


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
            else:
                return HttpResponse("Incorrect login or password", status=401)
            
        except KeyError:
            return HttpResponse("JSON format is incorrect. Please provide username and password", status=400)

        return HttpResponse(status=200)

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

def test(request):
    print(request.user.id)
    return HttpResponse(status=200)
    

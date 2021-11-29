from django.template import loader
from django.http import HttpResponse
from movies.models import Movies, People, Directors, User
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
    return HttpResponse(movie)

# =======================================================================================================

# People ================================================================================================

# Get all people
def getPeople(request):
    people_list = list(People.objects.all().values())
    return HttpResponse(people_list)
# Get person by id
def getPeopleById(request, person_id):
    person = People.objects.filter(id=person_id).values()
    return HttpResponse(person)

# =======================================================================================================

# Directors # ===========================================================================================

# Get all directors
def getDirectors(request):
    directors_list = list(Directors.objects.all().values())
    return HttpResponse(directors_list)


def getDirectorsByMovieId(request, movie_id):
    directors_by_movie = Directors.objects.filter(movie_id=movie_id).values()
    return HttpResponse(directors_by_movie)


def getDirectorsByPersonId(request, person_id):
    directors_by_person = Directors.objects.filter(
        person_id=person_id).values()
    return HttpResponse(directors_by_person)

def getUsers(request):
    if request.method == 'PUT':
        json_data = json.loads(request.body)
        try:
            user = User()
            # If json data doesn't exist return autoamtically returns 500
            username = json_data['username']
            email = json_data['email']
            password = json_data['password']
            user.username = username
            user.email = email
            user.password = password
            # If unique constrains fail server will return 500
            user.save()
        except KeyError:
            return HttpResponse(status=500)

        return HttpResponse(status=200)
    

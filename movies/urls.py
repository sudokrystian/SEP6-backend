from django.urls import path

from . import views

urlpatterns = [
    path('', views.getIndex, name='Main page'),
    # /movies/
    path('movies', views.getMovies, name='All movies'),
    # /movies/{movie_id}/
    path('movies/<int:movie_id>/', views.getMovieById, name='Movie by ID'),
    # /people/
    path('people', views.getPeople, name='All people'),
    # /people/{person_id}/
    path('people/<int:person_id>/', views.getPeopleById, name='People by ID'),
    # /directors/
    path('directors', views.getDirectors, name='All directors'),
    # /directors/movies/{movie_id}
    path('directors/movies/<int:movie_id>', views.getDirectorsByMovieId, name='Director by movie ID'),
    # /directors/people/{person_id}
    path('directors/people/<int:person_id>', views.getDirectorsByPersonId, name='Director by person ID'),
    # /register
    path('register', views.registerUser, name='Register the user'),
    # /login
    path('login', views.becomeUser, name='Login'),
    # /logout
    path('logout', views.logout_from_service, name='Logout'),
    # /users This one will be deleted but for now it is running only if you are authenticated
    path('users', views.getUsers, name='Get all users'),
    
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.getIndex, name='Main page'),
    
    # Movies ================================================================================================
    # /movies/
    path('movies', views.getMovies, name='All movies'),
    # /movies/{movie_id}/
    path('movies/<int:movie_id>/', views.getMovieById, name='Movie by ID'),

    # People ================================================================================================
    # /people/
    path('people', views.getPeople, name='All people'),
    # /people/{person_id}/
    path('people/<int:person_id>/', views.getPeopleById, name='People by ID'),

    # Directors =============================================================================================
    # /directors/
    path('directors', views.getDirectors, name='All directors'),
    # /directors/movies/{movie_id}
    path('directors/movies/<int:movie_id>', views.getDirectorsByMovieId, name='Director by movie ID'),
    # /directors/people/{person_id}
    path('directors/people/<int:person_id>', views.getDirectorsByPersonId, name='Director by person ID'),

    # Ratings ==============================================================================================
    path('rating', views.getAllRatings, name='Get all ratings'),
    path('ratings/movies/<int:movie_id>', views.getRating, name='Get all ratings for the movie'),
    path('rating/movies/<int:movie_id>', views.getRating2, name='Get all ratings for the movie'),
    path('rating/populate', views.populateRatings, name='Ugabuga'),


    # User =================================================================================================
    # /register
    path('register', views.registerUser, name='Register the user'),
    # /login
    path('login', views.becomeUser, name='Login'),
    # /logout
    path('logout', views.logout_from_service, name='Logout'),
    # /users This one will be deleted but for now it is running only if you are authenticated
    path('users', views.getUsers, name='Get all users'),
    # test
    path('test', views.test, name="test")
    
]
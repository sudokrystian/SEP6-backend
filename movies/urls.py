from django.urls import path

from . import views

urlpatterns = [
    path('', views.getIndex, name='Main page'),
    
    # Movies ================================================================================================
    # /movies/{movie_id}/
    path('movies/<int:movie_id>/', views.getMovieById, name='Movie by ID'),
    # /movies/{movie_id}/credits
    path('movies/<int:movie_id>/credits', views.getMovieCrew, name='Movie by ID'),
    # /movies/trading
    path('movies/trending', views.getTrendingMovies, name='Get trading movies'),

    # People ================================================================================================
    # /people/{person_id}/
    path('people/<int:person_id>/', views.getPersonById, name='Get person by ID'),

    # Ratings ==============================================================================================
    # rating/movies/{movie_id}
    path('rating/movie/<int:movie_id>', views.getRatingsByMovie, name='Get all ratings for the movie'),
    # /rating/user/{movie_id}
    path('rating/user/<int:movie_id>', views.getUserRatingForTheMovie, name='Get rating for the movie for the user'),
    # /rating/user
    path('rating/user', views.getRatingsByUser, name='Get all user ratings'),

    # /rating
    path('rating', views.addRating, name='Adds rating to the movie'),
  

    # Movie lists ==========================================================================================
    # /list
    path('list', views.movieLists, name='Find the lists for the user or create a new one'),

    # User =================================================================================================
    # /register
    path('register', views.registerUser, name='Register the user'),
    # /login
    path('login', views.becomeUser, name='Login'),
    # /logout
    path('logout', views.logout_from_service, name='Logout'),
]
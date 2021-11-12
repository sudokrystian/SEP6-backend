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
]
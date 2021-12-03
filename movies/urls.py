from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # Main page
    path('', views.getIndex, name='Main page'),

    # Movies ================================================================================================
    # /movies/{movie_id}/
    path('movies/<int:movie_id>/', views.MovieById.as_view(), name='Movie by ID'),
    # /movies/{movie_id}/credits
    path('movies/<int:movie_id>/credits', views.MovieCrew.as_view(), name='Get movie crew'),
    # /movies/trending
    path('movies/trending', views.TrendingMovies.as_view(), name='Get trending movies'),
    # /search/movie/page/<int:page>/name/<str:name>
    path('search/movie/page/<int:page_number>/name/<str:movie_name>', views.MovieByName.as_view(), name='Find movie by name'),

    # People ================================================================================================
    # /people/{person_id}/
    path('people/<int:person_id>/', views.PersonById.as_view(), name='Get person by ID'),
    # search/people/page/<int:page>/name/<str:name>
    path('search/people/page/<int:page_number>/name/<str:person_name>', views.PeopleByName.as_view(), name='Find people by name`'),


    # Ratings ==============================================================================================
    # rating/movies/{movie_id}
    path('rating/movie/<int:movie_id>', views.MovieRating.as_view(), name='Get all ratings for the movie'),
    # /rating/user/{movie_id}
    path('rating/user/<int:movie_id>', views.UserMovieRating.as_view(), name='Get rating for the movie for the user'),
    # /rating/user
    path('rating/user', views.UserRatings.as_view(), name='Get all user ratings'),
    # /rating
    path('rating', views.AddRating.as_view(), name='Adds rating to the movie'),
  

    # Movie lists ==========================================================================================
    # /list
    path('list', views.MovieLists.as_view(), name='Find the lists for the user or create a new one'),

    # User =================================================================================================
    # /register
    path('register', views.RegisterUser.as_view(), name='Register the user'),
    # Token (login) ===================================
    # Obtain JWT token
    # api/token/
    path('login', jwt_views.TokenObtainPairView.as_view(), name='Obtain the token'),
    # Refresh JWT token
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='Refresh the token'),
]
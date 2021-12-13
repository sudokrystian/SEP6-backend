from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # Main page
    path('', views.getIndex, name='Main page'),

    # Movies ================================================================================================
    # /movies/{movie_id}/
    path('movies/<int:movie_id>/', views.MovieById.as_view(), name='Movie by ID'),
    # /movies/{movie_id}/images
    path('movies/<int:movie_id>/images', views.MovieImg.as_view(), name='Get movie mages by movie ID'),
    # /movies/{movie_id}/credits
    path('movies/<int:movie_id>/credits', views.MovieCrew.as_view(), name='Get movie crew'),
    # /movies/{movie_id}/similar
    path('movies/<int:movie_id>/similar', views.MovieSimilar.as_view(), name='Get similar movies'),
    # /movies/trending
    path('movies/trending', views.TrendingMovies.as_view(), name='Get trending movies'),
    # /search/movie/page/{page_number}/name/{movie_name}
    path('search/movie/page/<int:page_number>/name/<str:movie_name>', views.MovieByName.as_view(), name='Find movie by name'),

    # People ================================================================================================
    # people/{person_id}/
    path('people/<int:person_id>/', views.PersonById.as_view(), name='Get person by ID'),
    # people/trending
    path('people/trending', views.TrendingPeople.as_view(), name='Get trending people'),
    # search/people/page/{page_number}/name/{person_name}
    path('search/people/page/<int:page_number>/name/<str:person_name>', views.PeopleByName.as_view(), name='Find people by name`'),
    # people/{person_id}/credits
    path('people/<int:person_id>/credits', views.PersonCredits.as_view(), name='Get credits for the person'),


    # Ratings ==============================================================================================
    # rating/movies/{movie_id}
    path('rating/movie/<int:movie_id>', views.MovieRating.as_view(), name='Get all ratings for the movie'),
    # /rating/person
    path('rating/person/<int:person_id>', views.PersonAverageMovieRating.as_view(), name='Get average person rating'),
    # /rating/user/{movie_id}
    path('rating/user/<int:movie_id>', views.UserMovieRating.as_view(), name='Get rating for the movie for the user'),
    # /rating/user
    path('rating/user', views.UserRatings.as_view(), name='Get all user ratings'),
    # /rating
    path('rating', views.AddRating.as_view(), name='Adds rating to the movie'),
  

    # Movie lists ==========================================================================================
    # /list
    path('list', views.MovieLists.as_view(), name='Find the lists for the user or create a new one'),
    # /list/{list_id}>
    path('list/<int:list_id>', views.MovieListDelete.as_view(), name='Delete the list'),
    # /list/details
    path('list/details', views.MovieListsDetails.as_view(), name='Find detailed lists for the user'),
    # /list/{list_id}/movies
    path('list/<int:list_id>/movies', views.MoviesInList.as_view(), name='Find the movies for the specified list'),
    # /list/movies
    path('list/movies', views.MovieAddToList.as_view(), name='Add movie to the existing list'),
    # /list/{list_id}/movies/{movie_id}
    path('list/<int:list_id>/movies/<int:movie_id>', views.MovieDeleteFromList.as_view(), name='Delete movie from an existing list'),

    # Comments =================================================================================================
    # /movies/{movie_id}/comments
    path('movies/<int:movie_id>/comments', views.Comments.as_view(), name='Get comments for the movie'),
    # /movies/{movie_id}/comments
    path('movies/comments', views.CommentAdd.as_view(), name='Add comment to the movie'),

    # User =================================================================================================
    # /register
    path('register', views.RegisterUser.as_view(), name='Register the user'),
    # Token (login) ===================================
    # Obtain JWT token
    # api/token/
    path('login', jwt_views.TokenObtainPairView.as_view(), name='Obtain the token'),
    # Refresh JWT token
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='Refresh the token'),

    # Development ===========================================================================================
    path('fakeratings', views.test, name="Adds fake data to ratings")
]
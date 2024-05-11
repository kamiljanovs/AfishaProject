from django.urls import path
from . import views

urlpatterns = [
    # path('', views.movie_list_api_view),
    path('', views.MovieListAPIView.as_view()),

    # path('<int:id>/', views.movie_api_view),
    path('<int:id>/', views.MovieDetailAPIView.as_view()),

    # path('reviews/', views.movie_list_api_view),

    path('directors/', views.DirectorListAPIView.as_view()),
    path('directors/<int:id>/', views.DirectorDetailAPIView.as_view()),

    path('reviews/', views.ReviewModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reviews/<int:id>/', views.ReviewModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

#     path('directors/', views.director_list_api_view),
#     path('directors/<int:id>/', views.director_api_view),
#
#     path('reviews/', views.review_list_api_view),
#     path('reviews/<int:id>/', views.review_api_view),
]
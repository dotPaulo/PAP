from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from appPAP.views import *

urlpatterns = [
    # Admin Painel
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    
    
    # Home
    path('', Home.as_view(), name='home'),
    path('eula', EULA.as_view(), name='eula'),

    # Account Painel
    path('accounts/', include('allauth.urls')),

    # Perfis
    path('profiles/', ProfileListView, name='profile_list'),
    path('profiles/create/', ProfileCreateView.as_view(), name='profile_create'),
    path("profile/edit/", ProfileEditSelection.as_view(), name="profile_editSelection"),
    path("profile/edit/<uuid:profile_id>", ProfileEdit.as_view(), name="profile_edit"),
    path('profile/<uuid:profile_uuid>/login/', profile_login, name='profile_login'),

    # Filmes
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/fav', list_favorites, name='movie_fav'),
    path('movies/wl', list_wl, name='movie_wl'),
    path('movies/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movies/<uuid:movie_id>/edit/', MovieUpdateView.as_view(), name='movie_edit'),
    path('movies/select/', MovieSelectionView.as_view(), name='movie_select'),
    path('movie/play/<str:movie_id>/',ShowMovie.as_view(),name='play'),
    path('movie/detail/<str:movie_id>/',ShowMovieDetail.as_view(),name='show_det'),
    path('movie/category/<str:category>/',category_movies,name='show_movie_category'),

    # Videos
    path('videos/create/', VideoCreateView.as_view(), name='video_create'),


    # Ações do usuário
    path('movies/<int:movie_id>/watchlater/add/', add_to_watch_later, name='add_to_watch_later'),
    path('movies/<int:movie_id>/watchlater/remove/', remove_from_watch_later, name='remove_from_watch_later'),
    path('movies/<int:movie_id>/favorites/add/', add_to_favorites, name='add_to_favorites'),
    path('movies/<int:movie_id>/favorites/remove/', remove_from_favorites, name='remove_from_favorites'),

    #Watch
    path('watch/<uuid:profile_id>/', Watch.as_view(), name='watch'),

    #Busca
    path('search/', search_results, name='search_results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
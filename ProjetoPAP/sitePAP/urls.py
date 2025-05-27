from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from appPAP.views import (
    Home,
    ProfileListView, ProfileCreateView, ProfileDeleteView, ProfileEditSelection, ProfileEdit,
    MovieListView, MovieCreateView, MovieUpdateView, MovieDeleteView, Watch,
    add_to_watch_later, remove_from_watch_later, add_to_favorites, profile_login, admin_dashboard
)

urlpatterns = [
    # Admin Painel
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    
    # Home
    path('', Home.as_view(), name='home'),

    # Account Painel
    path('accounts/', include('allauth.urls')),

    # Perfis
    path('profiles/', ProfileListView, name='profile_list'),
    path('profiles/create/', ProfileCreateView.as_view(), name='profile_create'),
    path('profiles/delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile_delete'),
    path("profile/edit/", ProfileEditSelection.as_view(), name = "profile_editSelection"),
    path("profile/edit/<uuid:profile_id>", ProfileEdit.as_view(), name = "profile_edit"),
    path('profile/<uuid:profile_uuid>/login/', profile_login, name='profile_login'),

    # Filmes
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movies/<int:pk>/edit/', MovieUpdateView.as_view(), name='movie_edit'),
    path('movies/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),

    # Ações do usuário
    path('movies/<int:movie_id>/watchlater/add/', add_to_watch_later, name='add_to_watch_later'),
    path('movies/<int:movie_id>/watchlater/remove/', remove_from_watch_later, name='remove_from_watch_later'),
    path('movies/<int:movie_id>/favorites/add/', add_to_favorites, name='add_to_favorites'),

    #Watch
     path('watch/<uuid:profile_id>/',Watch.as_view(),name='watch'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
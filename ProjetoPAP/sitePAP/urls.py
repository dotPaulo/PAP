"""
URL configuration for sitePAP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from appPAP.views import *
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
    path('accounts/', include('allauth.urls')),  
    
    # Perfil
    path('profile/', ProfileListView.as_view(), name='profile_list'),
    path('profile/create/', ProfileCreateView.as_view(), name='profile_create'),
    path('profile/delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile_delete'),

    # Filmes
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movies/update/<int:pk>/', MovieUpdateView.as_view(), name='movie_update'),
    path('movies/delete/<int:pk>/', MovieDeleteView.as_view(), name='movie_delete'),

    # Categorias
    path('movies/category/<str:categoria>/', WatchCategory_view, name='watch_category'),

    # Ações de filme
    path('movies/<int:movie_id>/watch_later/add/', add_to_watch_later, name='add_to_watch_later'),
    path('movies/<int:movie_id>/watch_later/remove/', remove_from_watch_later, name='remove_from_watch_later'),
    path('movies/<int:movie_id>/favorites/add/', add_to_favorites, name='add_to_favorites'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
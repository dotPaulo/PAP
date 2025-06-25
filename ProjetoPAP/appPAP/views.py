from typing import Self
from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from .models import *
from .forms import *

User = get_user_model()


# Home 
class Home(View):
    def get(self, request, *args, **kwargs):
        trending_movies = Movie.objects.order_by('-created')[:10]  # Pega os 10 filmes mais recentes
        return render(request, 'index.html', {'trending_movies': trending_movies})

class EULA(View):

    template_name = 'EULA.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'EULA.html')


"""
  FUNCIONALIDADES DO ADMINISTRADOR
"""

"""
  Dashboard do Administrador 
"""

@login_required
def admin_dashboard(request):
    if not request.user.groups.filter(name__in=['Administrador', 'Coordenador']).exists():
        return render(request, '404.html')

    # Contar dados
    total_users = Profile.objects.count()
    total_movies = Movie.objects.filter(type='Documentário').count()

    context = {
        'total_users': total_users,
        'total_movies': total_movies,

    }
    return render(request, 'admin/dashboard.html', context)


def dashboard_view(request):
    profile_count = Profile.objects.count()
    movie_count = Movie.objects.count()

    context = {
        'total_users': profile_count,
        'movie_count': movie_count,
    }

    return render(request, 'dashboard.html', context)


"""
    FUNCIONALIDADES DE FILMES
"""


class MovieListView(ListView):
    model = Movie
    template_name = 'movieList.html'
    context_object_name = 'movies'

class MovieCreateView(UserPassesTestMixin, CreateView):
    model = Movie
    template_name = 'admin/movieCreate.html'
    form_class = MovieForm
    success_url = reverse_lazy('movie_select')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Filme criado com sucesso!')
        return response

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class MovieUpdateView(UserPassesTestMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'admin/movieEdit.html'
    success_url = reverse_lazy('movie_select')
    pk_url_kwarg = 'movie_id'
    slug_field = 'uuid'
    slug_url_kwarg = 'movie_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Movie, uuid=self.kwargs['movie_id'])

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            movie = self.get_object()
            movie.delete()
            messages.success(request, 'Filme deletado com sucesso!')
            return redirect('movie_select')
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Filme atualizado com sucesso!')
        return response

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class MovieSelectionView(ListView):
    model = Movie
    template_name = 'admin/movieEditSelection.html'
    context_object_name = 'movies'

    def get_object(self, queryset=None):
        return get_object_or_404(Movie, uuid=self.kwargs['movie_id'])

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

"""
    FUNCIONALIDADES DE VIDEOS
"""

class VideoCreateView(CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'admin/videoCreate.html'
    success_url = reverse_lazy('admin_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Vídeo criado com sucesso!')
        return response

"""
    FUNCIONALIDADES DE PERFIL
"""


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['name', 'role', 'email', 'password']
    template_name = 'admin/profileCreate.html'
    success_url = '/profile/edit/'

    def form_valid(self, form):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        role = self.request.POST.get('role')

        if not email or not password:
            form.add_error(None, 'Email e senha são obrigatórios.')
            return self.form_invalid(form)

        # Verifica se já existe usuário
        user, created = User.objects.get_or_create(username=email, defaults={
            'email': email,
            'password': make_password(password),
        })

        if not created:
            user.password = make_password(password)
            user.save()

        # Grupos
        if role in ['Administrador', 'Coordenador']:
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.clear()
            user.groups.add(group)

        # Permissões especiais
        if role == 'Administrador':
            user.is_staff = True
            user.is_superuser = False  # Ou True se quiser controle total
            user.save()

        # Cria profile e associa user
        profile = form.save(commit=False)
        profile.user = user
        profile.password = make_password(password)
        profile.save()

        # Relaciona profile ao usuário logado (se necessário)
        self.request.user.profiles.add(profile)

        messages.success(self.request, 'Perfil criado com sucesso!')
        return redirect(self.success_url)

class ProfileEditSelection(LoginRequiredMixin, View):
    def get(self, request):
        profiles = Profile.objects.all()
        return render(request, 'admin/profileEditSelection.html', {'profiles': profiles})


class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ['name', 'role', 'password', 'email']
    template_name = 'admin/profileEdit.html'
    pk_url_kwarg = 'profile_id'
    success_url = reverse_lazy('profile_editSelection')

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, uuid=self.kwargs['profile_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            profile = self.get_object()
            profile.delete()
            messages.success(request, 'Perfil deletado com sucesso!')
            return redirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return response

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

"""
    FUNCIONALIDADES DE USUARIO
"""

"""
    FUNCIONALIDADES DE LOGIN DE PERFIL 
"""


def profile_login(request, profile_uuid):
    profile = get_object_or_404(Profile, uuid=profile_uuid)

    request.session['current_profile_uuid'] = str(profile.uuid)

    if request.method == 'POST':
        password = request.POST.get('password')

        if check_password(password, profile.password):  # Verifica o hash
            request.session['profile_access'] = str(profile.uuid)
            return redirect('watch', profile_id=profile.uuid)
        else:
            messages.error(request, 'Senha incorreta. Tente novamente.')

    return render(request, 'profile_login.html', {'profile': profile})


def ProfileListView(request):
    profiles = Profile.objects.all()
    return render(request, 'profileList.html', {'profiles': profiles, 'show_navbar': False})


# Watch
class ShowMovie(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            movie = movie.videos.values()
            return render(request, 'showMovie.html', {'movie': list(movie)})
        except Movie.DoesNotExist:
            return render(request, '404.html')

class ShowMovieDetail(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            related_movies = Movie.objects.filter(type=movie.type).exclude(uuid=movie.uuid)
            return render(request, 'movieDetails.html', {'movie': movie, 'related_movies': related_movies})
        except Movie.DoesNotExist:
            return render(request, '404.html')

class Watch(View):
    def get(self, request, profile_id, *args, **kwargs):
        try:
            profile = Profile.objects.get(uuid=profile_id)
        except Profile.DoesNotExist:
            return render(request, '404.html')
        profile_access = request.session.get('profile_access')
        if profile_access != str(profile.uuid):
            return redirect('profile_login', profile_uuid=profile.uuid)
        movies = Movie.objects.all()
        showcase = movies[0] if movies else None
        return render(request, 'movieList.html', {
            'movies': movies,
            'show_case': showcase,
            'profile': profile,
        })

def category_movies(request, category):
    try:
        movies = Movie.objects.filter(type=category)
        return render(request, 'category_list.html', {'movies': movies, 'category': category})
    except Exception:
        return render(request, '404.html')

def add_to_watch_later(request, movie_id):
    profile_uuid = request.session.get('profile_access')
    if not profile_uuid:
        messages.error(request, "Nenhum perfil autenticado.")
        return render(request, '404.html')
    try:
        profile = get_object_or_404(Profile, uuid=profile_uuid)
        movie = get_object_or_404(Movie, pk=movie_id)
        profile.watch_later.add(movie)
        return redirect('watch', profile_id=profile.uuid)
    except Exception:
        return render(request, '404.html')

def remove_from_watch_later(request, movie_id):
    profile_uuid = request.session.get('profile_access')
    if not profile_uuid:
        messages.error(request, "Nenhum perfil autenticado.")
        return render(request, '404.html')
    try:
        profile = get_object_or_404(Profile, uuid=profile_uuid)
        movie = get_object_or_404(Movie, pk=movie_id)
        profile.watch_later.remove(movie)
        return redirect('movie_wl')
    except Exception:
        return render(request, '404.html')

def list_wl(request):
    profile_uuid = request.session.get('profile_access')
    if not profile_uuid:
        messages.error(request, "Nenhum perfil autenticado.")
        return render(request, '404.html')
    try:
        profile = get_object_or_404(Profile, uuid=profile_uuid)
        watch_later = profile.watch_later.all()
        return render(request, 'movieWL.html', {'movies': watch_later})
    except Exception:
        return render(request, '404.html')

def add_to_favorites(request, movie_id):
    profile_uuid = request.session.get('profile_access')
    if not profile_uuid:
        messages.error(request, "Nenhum perfil autenticado.")
        return render(request, '404.html')
    try:
        profile = get_object_or_404(Profile, uuid=profile_uuid)
        movie = get_object_or_404(Movie, pk=movie_id)
        profile.favorites.add(movie)
        return redirect('watch', profile_id=profile.uuid)
    except Exception:
        return render(request, '404.html')

def remove_from_favorites(request, movie_id):
    profile_uuid = request.session.get('profile_access')
    if not profile_uuid:
        messages.error(request, "Nenhum perfil autenticado.")
        return render(request, '404.html')
    try:
        profile = get_object_or_404(Profile, uuid=profile_uuid)
        movie = get_object_or_404(Movie, pk=movie_id)
        profile.favorites.remove(movie)
        return redirect('movie_fav')
    except Exception:
        return render(request, '404.html')

def list_favorites(request):
    profile_uuid = request.session.get('profile_access')
    if not profile_uuid:
        messages.error(request, "Nenhum perfil autenticado.")
        return render(request, '404.html')
    try:
        profile = get_object_or_404(Profile, uuid=profile_uuid)
        favorites = profile.favorites.all()
        return render(request, 'movieFav.html', {'movies': favorites})
    except Exception:
        return render(request, '404.html')

def search_results(request):
    query = request.GET.get('q', '')
    try:
        results = Movie.objects.filter(title__icontains=query) if query else []
        return render(request, 'search_results.html', {'query': query, 'results': results})
    except Exception:
        return render(request, '404.html')
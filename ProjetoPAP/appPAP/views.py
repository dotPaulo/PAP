from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile, Movie
from .forms import MovieForm
from django.contrib.auth.decorators import login_required

# ----------- View Home -----------

class Home(View):
    def get(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/profile/')
        return render(request,'index.html')

# ----------- Views de Perfil -----------
class ProfileListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'profiles'

class ProfileCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Profile
    fields = [] 
    template_name = 'profiles/profile_create.html'

    def test_func(self):
        return self.request.user.role == 'ADMIN_TEACHER'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'profiles/profile_delete.html'
    success_url = '/profiles/'

    def test_func(self):
        return self.request.user.role == 'ADMIN_TEACHER'

# ----------- Views de Filme -----------
class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'

class MovieCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Movie
    form_class = MovieForm  
    template_name = 'movies/movie_create.html'

    def test_func(self):
        # Somente professores admin podem criar filmes
        return self.request.user.role == 'ADMIN_TEACHER'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_update.html'

    def test_func(self):
        # Somente o admin pode editar
        return self.request.user.role == 'ADMIN_TEACHER'

class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    template_name = 'movies/movie_delete.html'
    success_url = '/movies/'

    def test_func(self):
        return self.request.user.role == 'ADMIN_TEACHER'
    
def WatchCategory_view(request, categoria):
    movies = Movie.objects.filter(type = categoria)
    return render(request, 'watch_category.html', {'movies': movies})

# ----------- Ações de Filme (Ver Depois / Favoritos) -----------
@login_required
def add_to_watch_later(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    profile = request.user.profile
    profile.watch_later.add(movie)
    return redirect('movie_list')

@login_required
def remove_from_watch_later(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    profile = request.user.profile
    profile.watch_later.remove(movie)
    return redirect('movie_list')

@login_required
def add_to_favorites(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    profile = request.user.profile
    profile.favorites.add(movie)
    return redirect('movie_list')

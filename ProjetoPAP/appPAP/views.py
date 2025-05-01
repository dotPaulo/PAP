from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile, Movie
from .forms import MovieForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
# ----------- View Home -----------

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile_list')  # Use o nome da URL ou '/profiles/'
        return render(request, 'index.html')

# ----------- Views de Perfil -----------
class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profileList.html'
    context_object_name = 'profile'
    def test_func(self):
        return self.request.user.role == 'ADMIN_TEACHER'

class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = [] 
    template_name = 'profileCreate.html'
    
    success_url = '/profile/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_admin_fields'] = False
        if self.request.method == 'POST' and self.request.POST.get('role') == 'ADMIN_TEACHER':
            context['show_admin_fields'] = True
        return context

    def form_valid(self, form):
        # Verifique se os campos de admin foram preenchidos e validados
        if form.data.get('role') == 'ADMIN_TEACHER':
            admin_user = form.data.get('admin_user')
            admin_password = form.data.get('admin_password')

            if not admin_user or not admin_password:
                messages.error(self.request, "Por favor, preencha o usuário e senha de administrador.")
                return self.form_invalid(form)  # Redisplay o formulário com erros

            # Aqui você precisa validar as credenciais do admin
            # Exemplo:
            # admin = authenticate(username=admin_user, password=admin_password)
            # if admin is None or admin.role != 'ADMIN':
            #     messages.error(self.request, "Credenciais de administrador inválidas.")
            #     return self.form_invalid(form)
            
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'profileDelete.html'
    success_url = '/profile/'

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

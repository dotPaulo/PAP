from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import Profile, Movie
from .forms import MovieForm


# Home 
class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile_list')
        
        trending_movies = Movie.objects.order_by('-created')[:10]  # Pega os 10 filmes mais recentes
        return render(request, 'index.html', {'trending_movies': trending_movies})

#Admin
@login_required
def admin_dashboard(request):
    if request.user.username != 'administrador':
        return redirect('unauthorized')  # Crie uma view/template para acesso negado

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

#Profile
def profile_login(request, profile_uuid):
    profile = get_object_or_404(Profile, uuid=profile_uuid)
    
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
    return render(request, 'profileList.html', {'profiles': profiles})

class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['name', 'role']
    template_name = 'profileCreate.html'
    success_url = '/profiles/'

    def form_valid(self, form):
        password = self.request.POST.get('password')
        if not password:
            form.add_error('password', 'A senha é obrigatória.')
            return self.form_invalid(form)

        profile = form.save(commit=False)
        profile.password = make_password(password)  # Aplica o hash
        profile.save()

        self.request.user.profiles.add(profile)
        return redirect(self.success_url)

class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'profileDelete.html'
    success_url = '/profiles/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    
class ProfileEditSelection(LoginRequiredMixin, View):
    def get(self, request):
        profiles = request.user.profiles.all()
        return render(request, 'profileEditSelection.html', {'profiles': profiles})
        
class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['name', 'watch_later', 'favorites']
    template_name = 'profileEdit.html'
    pk_url_kwarg = 'profile_id'
    success_url = '/profiles/'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, uuid=self.kwargs['profile_id'], customuser=self.request.user)

    def form_valid(self, form):
        # Salva o perfil atualizado
        form.save()
        return redirect('profile_list')

#Movie
class MovieListView(ListView):
    model = Movie
    template_name = 'movieList.html'
    context_object_name = 'movies'

class MovieCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movieCreate.html'
    success_url = '/movies/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movieUpdate.html'
    success_url = '/movies/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    template_name = 'movieDelete.html'
    success_url = '/movies/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

#Watch
@method_decorator(login_required, name='dispatch')
class Watch(View):
    def get(self, request, profile_id, *args, **kwargs):
        try:
            profile = Profile.objects.get(uuid=profile_id)
        except Profile.DoesNotExist:
            return redirect('profile_list')

        # Verifica se o profile pertence ao user
        if profile not in request.user.profiles.all():
            return redirect('profile_list')

        # Verifica se senha do profile foi validada
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

@login_required
def add_to_watch_later(request, movie_id):
    profile_uuid = request.session.get('profile_access')
    if not profile_uuid:
        messages.error(request, "Nenhum perfil autenticado.")
        return redirect('profile_list')

    profile = get_object_or_404(Profile, uuid=profile_uuid)
    movie = get_object_or_404(Movie, pk=movie_id)
    profile.watch_later.add(movie)
    return redirect('watch', profile_id=profile.uuid)


@login_required
def remove_from_watch_later(request, movie_id):
    profile_uuid = request.session.get('profile_access')
    if not profile_uuid:
        messages.error(request, "Nenhum perfil autenticado.")
        return redirect('profile_list')

    profile = get_object_or_404(Profile, uuid=profile_uuid)
    movie = get_object_or_404(Movie, pk=movie_id)
    profile.watch_later.remove(movie)
    return redirect('watch', profile_id=profile.uuid)


@login_required
def add_to_favorites(request, movie_id):
    profile_uuid = request.session.get('profile_access')
    if not profile_uuid:
        messages.error(request, "Nenhum perfil autenticado.")
        return redirect('profile_list')

    profile = get_object_or_404(Profile, uuid=profile_uuid)
    movie = get_object_or_404(Movie, pk=movie_id)
    profile.favorites.add(movie)
    return redirect('watch', profile_id=profile.uuid)

# Handlers de erro
def handler400(request, exception):
    return render(request, 'errors/400.html', status=400)

def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)

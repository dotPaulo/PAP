from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile, Movie
from .forms import MovieForm

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile_list')
        
        trending_movies = Movie.objects.order_by('-created')[:10]  # Pega os 10 filmes mais recentes
        return render(request, 'index.html', {'trending_movies': trending_movies})


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profileList.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return self.request.user.profiles.all()

class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['name', 'role']
    template_name = 'profileCreate.html'
    success_url = '/profiles/'

    def form_valid(self, form):
        profile = form.save()
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
    
    def get_queryset(self):
        # Retorna só os perfis associados ao usuário logado
        return self.request.user.profiles.all()
        
class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['name', 'watch_later', 'favorites']
    template_name = 'profile_edit.html'
    pk_url_kwarg = 'profile_id'
    success_url = '/profiles/'

class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'

class MovieCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_create.html'
    success_url = '/movies/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_update.html'
    success_url = '/movies/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    template_name = 'movies/movie_delete.html'
    success_url = '/movies/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class Watch(View):
    def get(self,request,profile_id,*args, **kwargs):
        try:
            profile=Profile.objects.get(uuid=profile_id)

            movies=Movie.objects.filter(age_limit=profile.age_limit)

            try:
                showcase=movies[0]
            except :
                showcase=None
            

            if profile not in request.user.profiles.all():
                return redirect(to='profile_list')
            return render(request,'movieList.html',{
                'movies':movies,'show_case':showcase
            })
        except Profile.DoesNotExist:
            return redirect(to='profile_list')


@login_required
def add_to_watch_later(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    profile = request.user.profiles.first()
    if not profile:
        messages.error(request, "Nenhum perfil selecionado.")
        return redirect('profile_list')
    profile.watch_later.add(movie)
    return redirect('movie_list')

@login_required
def remove_from_watch_later(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    profile = request.user.profiles.first()
    if not profile:
        messages.error(request, "Nenhum perfil selecionado.")
        return redirect('profile_list')
    profile.watch_later.remove(movie)
    return redirect('movie_list')

@login_required
def add_to_favorites(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    profile = request.user.profiles.first()
    if not profile:
        messages.error(request, "Nenhum perfil selecionado.")
        return redirect('profile_list')
    profile.favorites.add(movie)
    return redirect('movie_list')

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def verificar_admin_password(request):
    if request.method == "POST":
        senha = request.POST.get("senha", "")
        if Profile.objects.filter(role="ADMIN_TEACHER", admin_password=senha).exists():
            return JsonResponse({"status": "ok"})
        return JsonResponse({"status": "erro", "mensagem": "Senha incorreta."})

# Handlers de erro
def handler400(request, exception):
    return render(request, 'errors/400.html', status=400)

def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)

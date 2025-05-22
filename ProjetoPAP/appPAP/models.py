from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

AGE_CLASS = [
    ('All', 'All'),
    ('Kids', 'Kids')
]

MOVIE_TYPE = [
    ('Documentário', 'Documentário'),
    ('Biografia', 'Biografia'),
    ('Histórico', 'Histórico'),
    ('Ciência e Natureza', 'Ciência e Natureza'),
    ('Educativo', 'Educativo'),
    ('Literário', 'Literário')
]

ROLE = [
    ('Administrador', 'Administrador'),
    ('Regular', 'Professor')
]

class CustomUser(AbstractUser):
    profiles = models.ManyToManyField('Profile')

    def __str__(self):
        return self.username

class Profile(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=15, choices=ROLE, default = 'Regular')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    watch_later = models.ManyToManyField('Movie', blank=True, related_name='watch_later_profiles')
    favorites = models.ManyToManyField('Movie', blank=True, related_name='favorite_profiles')
    age_limit = models.CharField(max_length=15, choices= AGE_CLASS, null= True, blank= True, default= 'All')
    admin_password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Movie(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    type = models.CharField(max_length=20, choices=MOVIE_TYPE)
    age_limit = models.CharField(max_length=15, choices= AGE_CLASS, null= True, blank= True, default='All')
    videos = models.ManyToManyField('Video')
    flyer = models.ImageField(upload_to='flyers', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

class Video(models.Model):
    titulo = models.CharField(max_length=125)
    file = models.FileField(upload_to='movies')

    def __str__(self):
        return self.titulo

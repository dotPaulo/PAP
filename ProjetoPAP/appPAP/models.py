from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


ROLE = [
    ('Administrador', 'Administrador'),
    ('Regular', 'Professor'),
    ('Coordenador', 'Coordenador'),
]

class CustomUser(AbstractUser):

    def __str__(self):
        return self.email or self.username

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profiles', blank='True', null='True')
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=15, choices=ROLE, default='Regular')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    watch_later = models.ManyToManyField('Movie', blank=True, related_name='watch_later_profiles')
    favorites = models.ManyToManyField('Movie', blank=True, related_name='favorite_profiles')
    password = models.CharField(max_length=255,blank=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    type = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='movies')
    videos = models.ManyToManyField('Video')
    flyer = models.ImageField(upload_to='flyers', blank=True, null=True)
    banner = models.ImageField(upload_to='banners', default='banners/defaultbanner.jpg')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

class Video(models.Model):
    titulo = models.CharField(max_length=125)
    file = models.FileField(upload_to='movies')

    def __str__(self):
        return self.titulo

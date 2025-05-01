from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

MOVIE_TYPE = [
    ('Documentário', 'Documentário'),       
    ('Biografia', 'Biografia'),              
    ('Histórico', 'Histórico'),              
    ('Ciência e Natureza', 'Ciência e Natureza'), 
    ('Educativo', 'Educativo'),             
    ('Literário', 'Literário')               
]

#Abstração dos users pra diferenciar entre regualar e admin
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN_TEACHER', 'Professor Administrador'),
        ('REGULAR_TEACHER', 'Professor Regular'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='REGULAR_TEACHER',
        verbose_name='Tipo de Usuário'
        
    )
    class Meta:
        permissions = [
            ("can_view_all_users", "Can view all users"),
        ]
class Movie(models.Model):
    title:str=models.CharField(max_length=225)
    description:str=models.TextField()
    created =models.DateTimeField(auto_now_add=True)
    uuid=models.UUIDField(default=uuid.uuid4,unique=True)
    type=models.CharField(max_length=25,choices=MOVIE_TYPE)
    videos=models.ManyToManyField('Video')
    flyer=models.ImageField(upload_to='flyers',blank=True,null=True)

class Video(models.Model):
    titulo = models.CharField(max_length=125)
    file = models.FileField(upload_to='movies')  

class Profile(models.Model):
    name = models.CharField(max_length=50, blank= False, null= False)
    uuid = models.UUIDField(default=uuid.uuid4)
    watch_later = models.ManyToManyField(
        Movie,
        related_name='watch_later_profiles',
        blank=True,
        verbose_name='Ver Depois'
    )
    favorites = models.ManyToManyField(
        Movie,
        related_name='favorite_profiles',
        blank=True,
        verbose_name='Favoritos'
    )


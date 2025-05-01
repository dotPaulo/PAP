# -*- coding: utf-8 -*-

from appPAP.models import Profile
from django.forms import ModelForm
from django import forms
from .models import Movie

class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        exclude=['uuid']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

from django import forms
from .models import Movie, Video, ROLE
from django.contrib.auth import get_user_model

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'type', 'flyer', 'banner', 'videos']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['titulo', 'file'] 
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

CustomUser = get_user_model()

class CustomUserRegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Nome de utilizador")
    email = forms.EmailField(required=False, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, label="Confirmar Password")
    profile_name = forms.CharField(max_length=50, required=True, label="Nome do Perfil")
    role = forms.ChoiceField(choices=ROLE, required=True, label="Cargo")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalnum():
            raise forms.ValidationError("Alguns caracteres não podem ser utilizados.")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de utilizador já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            self.add_error("confirm_password", "As palavra-passes não coincidem.")

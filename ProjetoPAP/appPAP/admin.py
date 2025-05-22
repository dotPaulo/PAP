from django.contrib import admin
from .models import CustomUser, Profile, Movie, Video
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Perfis", {'fields': ('profiles',)}),
    )

admin.site.register(Profile)
admin.site.register(Movie)
admin.site.register(Video)

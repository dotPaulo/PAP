from django.contrib import admin
from .models import CustomUser, Profile, Movie, Video
from django.contrib.auth.admin import UserAdmin

class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    
admin.site.register(Profile)
admin.site.register(Movie)
admin.site.register(Video)

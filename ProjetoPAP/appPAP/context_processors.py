from .models import Profile, Movie, Video

def current_profile(request):
    profile = None
    if request.user.is_authenticated:
        profile_uuid = request.session.get('current_profile_uuid')
        if profile_uuid:
            try:
                profile = Profile.objects.get(uuid=profile_uuid)
            except Profile.DoesNotExist:
                pass
    return {'current_profile': profile}

def movie_categories(request):
    return {
        'movie_categories': Movie._meta.get_field('type').choices
    }

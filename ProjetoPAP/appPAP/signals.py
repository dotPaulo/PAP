# appPAP/signals.py
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out
from django.contrib import messages

@receiver(post_migrate)
def create_default_admin_user(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='administrador').exists():
        User.objects.create_user(
            username='administrador',
            email='adminuser@gmail.com',
            password='admin',
            is_staff=True,
            is_superuser=True
        )
        print("✅ Usuário administrador criado (username: adminuser@gmail.com / email: adminuser@gmail.com / senha: admin)")

@receiver(user_logged_out)
def on_user_logout(sender, request, user, **kwargs):
    if request:
        messages.success(request, "Logout realizado com sucesso!")

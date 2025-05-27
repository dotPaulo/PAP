# appPAP/signals.py
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_admin_user(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='administrador').exists():
        User.objects.create_user(
            username='administrador',
            password='admin',
            is_staff=True,
            is_superuser=True
        )
        print("✅ Usuário administrador criado (username: administrador / senha: admin)")

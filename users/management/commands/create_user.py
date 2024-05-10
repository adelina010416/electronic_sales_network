from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = input('Введите email: ')
        password = input('Введите пароль: ')
        user = User.objects.create(
            email=email,
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(password)
        user.save()

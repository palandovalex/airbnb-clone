from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed

from users.models import User


class Command(BaseCommand):
    help = "This command will remove empty avarars, and set some avatars to them"

    def handle(self, *args, **options):
        
        users = User.objects.all()
        for user in users:
            user.avatar=None

        self.stdout.write(
            self.style.SUCCESS(f'Avatars is cleaned!')
        )

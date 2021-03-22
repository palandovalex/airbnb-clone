from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed

from users.models import User


class Command(BaseCommand):
    help = "This command creates users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", "-How many fake user entries do you want to create?",
            default=1, type=int
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {
                          "is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(
            self.style.SUCCESS(f'{number} users created!')
        )

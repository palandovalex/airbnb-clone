"""Seed reviews module"""
import random

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten

from django_seed import Seed

from rooms import models as room_models
from users import models as user_models
from reviews import models as review_models


class Command(BaseCommand):
    """Seed reviews Command"""
    help = "This command inserts reviews in database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", "-How many reviews do you want to seed?", type=int, default=2
        )

    def handle(self, *args, **options):

        number = options.get("number", 1)
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(review_models.Review, number, {
            "user": lambda x: random.choice(users),
            "room": lambda x: random.choice(rooms),


            "accuracy": lambda x: random.randint(1, 5),
            "communication": lambda x: random.randint(1, 5),
            "cleanlines": lambda x: random.randint(1, 5),
            "location": lambda x: random.randint(1, 5),
            "check_in": lambda x: random.randint(1, 5),
            "value": lambda x: random.randint(1, 5)
        })
        created_reviews = seeder.execute()
        created_clean = flatten(list(created_reviews.values()))
        print(created_clean)

        self.stdout.write(
            self.style.SUCCESS(f'{number} reviews created!')
        )

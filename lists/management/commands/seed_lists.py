"""Seed lists module"""
import random

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten

from django_seed import Seed

from rooms import models as room_models
from users import models as user_models
from lists import models as list_models

NAME = "lists"


class Command(BaseCommand):
    """Seed lists Command"""
    help = f"This command inserts {NAME} in database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", f"-How many {NAME} do you want to seed?", type=int, default=2
        )

    def handle(self, *args, **options):

        number = options.get("number", 1)
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(list_models.List, number, {
            "user": lambda x: random.choice(users)
        })
        created = seeder.execute()
        cleaned = flatten(list(created.values()))

        for pk in cleaned:
            room_list = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 10): random.randint(11, 30)]
            room_list.rooms.add(*to_add)

        print(cleaned)

        self.stdout.write(
            self.style.SUCCESS(f'{number} {NAME} created!')
        )

"""Seed reservation module"""
import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten

from django_seed import Seed

from rooms import models as room_models
from users import models as user_models
from reservations import models as reservation_models

NAME = "reservation"


class Command(BaseCommand):
    """Seed reservation Command"""
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

        seeder.add_entity(reservation_models.Reservation, number, {
            "status": lambda x: random.choice(
                ["pending", "confirmed", "canceled"]
            ),
            "check_in": lambda x: datetime.now(),
            "check_out": lambda x: datetime.now()+timedelta(days=random.randint(3, 30)),
            "guest": lambda x: random.choice(users),
            "room": lambda x: random.choice(rooms),

        })
        seeder.execute()

        self.stdout.write(
            self.style.SUCCESS(f'{number} {NAME} created!')
        )

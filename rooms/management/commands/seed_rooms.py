import random

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten

from django_seed import Seed

from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "This command inserts rooms in database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", "-How many rooms do you want to seed?", type=int, default=2
        )

    def handle(self, *args, **options):

        number = options.get("number", 1)
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()

        all_amenities = room_models.Amenity.objects.all()
        all_facilities = room_models.Facility.objects.all()
        all_house_rules = room_models.HouseRule.objects.all()

        seeder.add_entity(room_models.Room, number, {
            "name": lambda x: seeder.faker.address(),
            "host": lambda x: random.choice(all_users),
            "room_type": lambda x: random.choice(room_types),
            "price": lambda x: random.randint(1, 3000),
            "guests": lambda x: random.randint(0, 10),
            "beds": lambda x: random.randint(1, 10),
            "bedrooms": lambda x: random.randint(1, 5),
            "baths": lambda x: random.randint(1, 5),

            # "amenities": lambda x: random.choice(all_amenities),
            # "facilities": lambda x: random.choice(all_facilities),
            # "house_rules": lambda x: random.choice(all_house_rules),
        })
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))
        print(created_clean)
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for _ in range(1, random.randint(4, 17)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1,31)}.webp",
                )
            for amenity in all_amenities:
                if random.randint(0, 20) % 8 == 0:
                    room.amenities.add(amenity)
            for facility in all_facilities:
                if random.randint(0, 20) % 3 == 0:
                    room.facilities.add(facility)
            for rule in all_house_rules:
                if random.randint(0, 20) % 4 == 0:
                    room.house_rules.add(rule)

        self.stdout.write(
            self.style.SUCCESS(f'{number} rooms created!')
        )

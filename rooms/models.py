from my_calendar import MyCalendar
from django.db import models
from django.urls import reverse
from django.utils import timezone

from django_countries.fields import CountryField

from core import models as core_models
from users import models as user_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):
    """"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    class Meta:
        verbose_name = "Room type"
        ordering = ["name"]


class Amenity(AbstractItem):
    """ Amenity object definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility Model definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"
        verbose_name_plural = "House Rules"


class Photo(core_models.TimeStampedModel):
    """ Photo model definition """

    caption = models.CharField(max_length=140)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey(
        "Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = "Photo"


class Room(core_models.TimeStampedModel):
    """ Room Model Defenition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()

    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE)
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(
        Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(
        Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(
        HouseRule, related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rooms:detail', kwargs={'pk': self.pk})

    def total_rating(self):
        reviews = self.reviews.all()
        all_ratings = []
        for review in reviews:
            all_ratings.append(review.rating_average())
        try:
            avg = sum(all_ratings)/self.reviews.count()
            return round(avg, 2)
        except ZeroDivisionError:
            return "no reviews"

    class Meta:
        verbose_name_plural = "Rooms"

    def save(self, *args, **kwargs):
        self.city = self.city.capitalize()
        if self.price < 0:
            return
        super().save(*args, **kwargs)  # Call the real save() method

    def get_first_photo(self):
        if self.photos.count()>0:
            photo, = self.photos.all()[:1]
            return photo.file.url
        else:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        urls = [photo.file.url for photo in photos]
        print(urls)
        return urls

    def get_absolute_url(self):
        return reverse('rooms:detail', kwargs={'pk': self.pk})

    def get_calendars(self):
        this_year = timezone.now().year
        this_month = timezone.now().month
        this_calendar = MyCalendar(this_year, this_month)
        next_year, next_month = this_year, this_month+1
        if this_month == 12:
            next_year, next_month = this_year+1, 1
            
        next_calendar = MyCalendar(next_year, next_month)
        return [this_calendar, next_calendar]

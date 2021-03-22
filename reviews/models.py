from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from core import models as core_models

from reservations import models as reserv_models


class Review(core_models.TimeStampedModel):
    """ Review Model Definition """
    review = models.TextField()
    accuracy = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    cleanlines = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    location = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    check_in = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE)
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE)

    def __str__(self):
        return f'Review for room "{self.room.name}" by user "{self.user}"'

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ('-created',)

        pass

    def get_review_authority(self):
        reservations = reserv_models.Reservation.objects.filter(room=self.room, guest=self.user)
        if reservations.count() == 0:
            return 0

        review_authority = 0
        review_authority += min(reservations.count(), 3)
        return review_authority
        #last_reservation = reservations.order_by('-check_out').first()
        #last_reserv_date = last_reservation.check_out


    def rating_average(self):
        average = (self.accuracy + self.communication +
                   self.cleanlines + self.location +
                   self.check_in + self.value)/6

        return round(average, 2)

    rating_average.short_description = "Avg."

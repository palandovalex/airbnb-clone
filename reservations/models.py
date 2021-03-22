import datetime

from django.db import models
from django.utils import timezone
from core import models as core_models

class BookedDay(core_models.TimeStampedModel):
    day = models.DateField()
    reservation = models.ForeignKey("Reservation", related_name="booked_days", on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return f"Booked Day {self.day} in reservation - {self.reservation}"


class ReservationError(Exception):
    pass


class Reservation(core_models.TimeStampedModel):
    """ Reservation Model Definition """
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"
    STATUS_CHOISE = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled")
    ]
    check_in = models.DateField()
    check_out = models.DateField()

    status = models.CharField(max_length=12, choices=STATUS_CHOISE, default=STATUS_PENDING)

    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE)
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE)

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out
    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        finished = now > self.check_out
        if finished:
            BookedDay.objects.filter(reservation=self).delete()
        return finished

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_res = Reservation.objects.get(pk=self.pk)
            if old_res.check_in == self.check_in and old_res.check_out == self.check_out:
                return super().save(*args, **kwargs)
            else:
                old_booked_days = BookedDay.objects.filter(reservation=old_res)
                old_booked_days.delete()
        
        start:datetime.date = self.check_in
        end: datetime.date = self.check_out
        print (start, end)
        if end < start:
            raise ValueError("Checkin must be befor of equal to Checkout")
        difference:datetime.timedelta = end - start
        
        exiting_booked_day = BookedDay.objects.filter(
            day__range=(start, end),
            reservation__room=self.room,
        ).exists()

        if not exiting_booked_day:
            result = super().save(*args, **kwargs)
            for i in range(difference.days + 1):
                day = start + datetime.timedelta(days=i)
                BookedDay.objects.create(day = day, reservation = self)
            return result
        else:
            raise ReservationError()


    def __str__(self):
        return f'Reservation of room "{self.room}" by user "{self.guest}"'

from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """ Reservation Admin Definition """
    list_display = ("room", "guest", "status", "check_in",
                    "check_out", "in_progress", "is_finished")
    list_filter = ("status", "check_in", "check_out")

    pass


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    """ BookedDay Admin Definition """
    list_display = ("day", "reservation")

    pass

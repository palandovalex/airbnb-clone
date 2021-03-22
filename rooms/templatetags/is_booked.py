from calendar import month
import datetime
from django import template
import django
from reservations import models as reserv_models

register = template.Library()


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    else:
        this_date = datetime.datetime(
            year=day.year, month=day.month, day=day.number, 
            hour=0, minute=0,second=0
        )

        #I hate this black magick! But with this it turns out much shorter than without it...
        booked_days = reserv_models.BookedDay.objects.filter(day=this_date, reservation__room=room)
        return booked_days.count() > 0
               

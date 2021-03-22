from core import models
from django.http.response import Http404
from django.views.generic.base import View
import datetime
from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import redirect, render, reverse

from . import models as reserv_models
from rooms import models as room_models
from users.mixins import LoggedInOnlyView
from reviews.forms import CreateReviewForm

class CreateError(Exception):
    pass


def createReservation(request: HttpRequest, room_pk, year, month, date):
    try:
        this_date = datetime.datetime(year=year, month=month, day=date)
        room = room_models.Room.objects.get(pk=room_pk)
        if reserv_models.BookedDay.objects.filter(day=this_date, reservation__room=room).count()>0:
            raise CreateError("Room allready reserved for this time")
        if room.host.pk == request.user.pk:
            raise CreateError("You can't reserve your own room!")
        if this_date<=datetime.datetime.now():
            CreateError("Can't reserve room for past!")
        try:
            new_reservation = reserv_models.Reservation.objects.create(
                guest=request.user,
                room = room,
                check_in = this_date,
                check_out = this_date + datetime.timedelta(days=1),
            )
        except reserv_models.ReservationError:
            raise CreateError("cant create")
        messages.success(request, "Reservation created!")
        new_reservation.save()
        return redirect(reverse("reservations:detail", kwargs={"pk": new_reservation.pk}))
    except room_models.Room.DoesNotExist:
        messages.error(request, "This room does not exist!")
        return redirect(reverse("core:home"))
    except CreateError as e:
        messages.error(request, str(e))
        return redirect(reverse("core:home"))


class ReservationDetailView(LoggedInOnlyView, View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        user = self.request.user
        reservation = reserv_models.Reservation.objects.get(pk=pk)
        if reservation is None or (user != reservation.room.host and user != reservation.guest):
            raise Http404
        form = CreateReviewForm()
        return render(
            self.request, "reservations/detail.html", {"reservation": reservation, "form": form}
        )


def edit_reservation(request, pk, verb):
    reservation = reserv_models.Reservation.objects.get_or_none(pk=pk)
    user = request.user
    if not reservation or (user != reservation.guest and user != reservation.room.host):
        raise Http404()
    
    if verb == "confirm":
        if user != reservation.room.host:
            messages.error("Guests can't confirm they own reservations!")
            return redirect(reverse("core:home"))
        reservation.status = reserv_models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = reserv_models.Reservation.STATUS_CANCELED
        reserv_models.BookedDay.objects.filter(reservation=reservation).delete()

    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail"))

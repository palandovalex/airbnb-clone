from django.shortcuts import redirect, reverse, render
from django.http import HttpRequest, Http404
from django.contrib import messages


from rooms import models as room_models
from . import forms
# Create your views here.

def create_review(request: HttpRequest, room_pk:int):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.ger_or_none(pk=room_pk)
        if room is None:
            messages.warning("That room is not found.")
            return redirect(reverse("core:home"))
        if room.host.pk == request.user.pk:
            messages.error("You can't write reviews for your rooms!")
            return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
        if form.is_valid():
            review = form.save()
            review.user = request.user
            review.room = room
            review.save()
            messages.success(request, "Room reviewed")
            return redirect(reverse("rooms:detail", kwargs={"pk":room_pk}))
        else:
            return redirect(request.path_info)

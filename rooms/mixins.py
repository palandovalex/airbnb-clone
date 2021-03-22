
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import request
from django.shortcuts import redirect, reverse
from django.urls.base import reverse_lazy
from . import models as room_models


class RoomOwnerOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        if not super().test_func():
            return False
        room_pk = self.kwargs.get("pk")
        if room_pk is None:
            room_pk = self.kwargs.get("room_pk")
        result = is_room_owner(self.request, room_pk)
        if not result:
            messages.error(request, "Can't access that room")
        return result




class PhotoOwnerOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        if not super().test_func():
            return False

        room_pk = self.kwargs.get("room_pk")
        photo_pk = self.kwargs.get("photo_pk")
        if not is_room_owner(self.request, room_pk):
            return False
        try:
            photo = room_models.Photo.objects.get(pk=photo_pk)
            result = room_pk == photo.room.pk
                
        except room_models.Photo.DoesNotExist:
            result = False
        if not result:
            messages.error(self.request, "Can't access that photo.")
        return result
         

def is_room_owner(request, room_pk):
    user = request.user
    try:

        host = room_models.Room.objects.get(pk=room_pk).host
        return user.pk == host.pk
    except room_models.Room.DoesNotExist:
        return False
    

def photo_owner_required(func):
    def new_func(request, room_pk, photo_pk):
        test = PhotoOwnerOnlyMixin()
        test.request = request
        test.kwargs = {"room_pk": room_pk, "photo_pk": photo_pk}
        if test.test_func():
            return func(request, room_pk, photo_pk)
        else:
            return redirect(reverse("core:home"))
    
    return new_func

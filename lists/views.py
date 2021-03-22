from django.shortcuts import redirect, reverse, render
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http import HttpRequest
# Create your views here.
from rooms import models as room_models
from users import models as user_models
from . import models as list_models


def toggle_room(request: HttpRequest, room_pk):
    action = request.GET.get("action", None)
    user = request.user
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if not room:
        messages.error(request, _("Room not found"))
        return redirect(reverse("core:home"))
    if room.host == user:
        messages.warning(request, _(
            "You can't add your rooms to your favorite list"))
        return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
    
    the_list, __ = list_models.List.objects.get_or_create(
        name=list_models.List.FAVORITE_LIST_NAME,
        user=user
    )
    if action=="remove" and room in the_list.rooms.all():
        the_list.rooms.remove(room)
        messages.success(request, _("Room removed from favorits"))
    elif action=="add" and room not in the_list.rooms.all(): 
        the_list.rooms.add(room)
        messages.success(request, _(""))
    else:
        messages.warning(request. _("Somth ing went wrong"))
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavoritsView(TemplateView):
    template_name="lists/list_detail.html"
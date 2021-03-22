from django import template

from lists import models as list_models

register = template.Library()

@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    favs_list = list_models.List.objects.get_or_none(
        user=user,
        name=list_models.List.FAVORITE_LIST_NAME
    )
    
    return favs_list is not None and (room in favs_list.rooms.all())


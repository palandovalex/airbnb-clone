from django.http.response import Http404
from django.db.models import Q
from django.shortcuts import redirect, reverse, render
from django.views.generic import View
from django.http import HttpRequest
from django.contrib import messages
from django.utils.translation import gettext as _

from users import models as user_models
from . import models as convers_models

# Create your views here.


def go_convesation(request: HttpRequest, a_pk, b_pk):
    try:
        user_one = user_models.User.objects.get(pk=a_pk)
        user_two = user_models.User.objects.get(pk=b_pk)
    except user_models.User.DoesNotExist:
        messages.error(request, _("User not foud"))
        return redirect(reverse("core:home"))
    
    conversations = convers_models.Conversation.objects.filter(
        participants=user_one).filter(participants=user_two)
        
    if conversations.count()>1:
        raise NotImplementedError("Multiple conversations not implemented")
    elif conversations.count()==0:
        messages.success(request, _("Conversation created"))
        conversation = convers_models.Conversation.objects.create()
        conversation.participants.add(user_one, user_two)
    else:
        conversation = conversations[0]
    return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(View):
    model = convers_models.Conversation
    template_name = "conversations/detail.html"

    def check_access(self, *args, **kwargs):
        pk = kwargs["pk"]
        conversation = convers_models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404
        user = self.request.user
        if user not in conversation.participants.all():
            raise Http404
        return conversation, user


    def get(self, *args, **kwargs):
        conversation, user = self.check_access(*args, **kwargs)
        return render(
            request=self.request, 
            template_name=self.template_name,
            context={"conversation": conversation}
        )

    def post(self, *args, **kwargs):
        conversation, user = self.check_access(*args, **kwargs)
        message_content = self.request.POST.get("message_content")
        if not message_content:
            messages.error(request=self.request, message=_("How you could send empty message?!"))
        else:
            convers_models.Message.objects.create(
                conversation=conversation,
                user=user,
                content=message_content
            )
            messages.debug("succesfuly sended")
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))

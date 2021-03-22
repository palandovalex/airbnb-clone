from django.contrib.auth import mixins
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.urls.base import reverse_lazy


class LoggedOutOnlyView(UserPassesTestMixin):
    permission_denied_message = _("Page not found")
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.warning(self.request, _("Can't go there"))
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):
    permission_denied_message = _("Page not found")
    login_url = reverse_lazy("users:login")

    def handle_no_permission(self):
        messages.warning(self.request, _("Can't go there"))
        return redirect(reverse("core:home"))

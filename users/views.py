import os
from django.http.response import HttpResponse
import requests
from django.utils import translation
from django.core import files
from django.db import models
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import DateInput
from django.http import HttpRequest

from . import forms, mixins, models as user_models
from core.views import MyDateInput



class LoginView(mixins.LoggedOutOnlyView, View):
    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, "users/login.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        print("CSRF")
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", context={"form": form})

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next
        return reverse("core:home")
                
        

def logout_view(request):
    messages.info(request, "Sea you later!")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    
    template_name = "users/signup.html"
    form_class= forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        user.save()
        return super().form_valid(form)


def complite_verification(request, key):
    try:
        user = user_models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add succes message
        return redirect(reverse("core:home"))
    except user_models.User.DoesNotExist:
        # to do: add error message
        pass


class GithubException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        code = request.GET.get("code", None)
        client_secret = os.environ.get("GH_SECRET")
        if code is None:
            raise GithubException("code is None")
        token_request = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}", 
            headers={"Accept": "application/json"}
            )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise GithubException("Can't get access token")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json"
            },
        )
        profile_json: dict = profile_request.json()
        username = profile_json.get("login", None)
        if username is None:
            raise GithubException("username is None")
        print(profile_json)
        email = profile_json.get("email")
        if email is None:
            email_request = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json"
                },
            )
            print(email_request)
            raise GithubException("Your github account does not have public email.")
        first_name = profile_json.get("name")
        if first_name is None:
            first_name=""
        bio = profile_json.get("bio")
        if bio is None:
            bio = ""

        try:
            user = user_models.User.objects.get(email=email)
            if user_models.User.LOGIN_GITHUB not in user.login_method:
                raise GithubException(f"User with email={email} - can not log in by Github."+
                    "If you want to link accounts - you shoul login and configure your login methods."
                )
        except user_models.User.DoesNotExist:
            user = user_models.User.objects.create(
                username=email, first_name=first_name, bio=bio,
                email=email, email_verified=True,
                login_method=user_models.User.LOGIN_GITHUB
            )
            user.set_unusable_password()
            user.save()
        login(request, user)
        messages.success(request, f"Welcome back!")
        return redirect(reverse("core:home"))
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class GoogleException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def google_login(request):
    api_key = os.environ.get("GOOGLE_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/google/callback"
    messages.error(request, "Google auth not implemented")
    return redirect(reverse("users:login"))
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={api_key}&redirect_uri={redirect_uri}&response_type=code")


def google_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/google/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v1/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        email = profile_json.get("kaccount_email", None)
        if email is None:
            raise KakaoException("Please also give me your email")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGING_KAKAO:
                raise KakaoException(
                    f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGING_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        messages.success(request, f"Welcome back {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = user_models.User
    template_name='users/user_detail.html'
    context_object_name = "current_user"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = user_models.User
    template_name = 'users/update_profile.html'
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthday",
        "language",
        "currency"
    )
    success_message = "Profile Updated!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birthday"].widget = DateInput(format="%Y-%m-%d")
        print(form.fields["birthday"].widget)
        return form

    def get_object(self, queryset=None) -> models.Model:
        return self.request.user

    pass


class UpdatePasswordView(mixins.LoggedInOnlyView, SuccessMessageMixin, PasswordChangeView):
    template_name = "users/update_password.html"
    success_url = reverse_lazy('users:profile')
    success_message = "Password updated!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        user = self.request.user
        if user is None:
            return redirect(reverse("users:login"))
        if user_models.User.LOGIN_EMAIL in user.login_method:
            form.fields["old_password"].widget.attrs = {
            'placeholder': 'Current password'}
        else:
            form.fields["old_password"]=None
        form.fields["new_password1"].widget.attrs = {
            'placeholder': 'New password'}
        form.fields["new_password2"].widget.attrs = {
            'placeholder': 'Confirm new password'}
        return form
    

    def get_success_url(self) -> str:
        return self.request.user.get_absolute_url()


class UpdateAvatarView(UpdateView):
    model = user_models.User
    template_name = 'users/update_avatar.html'
    fields = ("avatar",)


@login_required
def switch_hosting(request):
    print(request.session.get("is_hosting"))
    if request.session.get("is_hosting") is None:
        request.session["is_hosting"] = True
    else:
        del request.session["is_hosting"]
    print(request.session.get("is_hosting"))
    return redirect(request.META.get('HTTP_REFERER'))


def switch_language(request: HttpRequest):
    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        print(f"lanuage - {lang}")
    return HttpResponse(status=200)

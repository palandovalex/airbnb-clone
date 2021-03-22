import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.forms import forms
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.shortcuts import reverse

from django.db import models

from . import models as user_models

# Create your models here.


class User(AbstractUser):
    """ Custom User Model """
    GENDER_MALE = "ml"
    GENDER_FEMALE = "fml"
    GENDER_UNSPECIFIED = "usp"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_UNSPECIFIED, _("Uncpecified"))
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_RUSSIAN = "ru"
    LANGUIGE_CHOICES = (
        (LANGUAGE_ENGLISH, _("English")),
        (LANGUAGE_RUSSIAN, _("Russian"))
    )

    CURRENCY_USD = "usd"
    CURRENCY_RUB = "rub"
    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_RUB, "RUB"))

    LOGIN_EMAIL = "em"
    LOGIN_GITHUB = "gh"
    LOGIN_KAKAO = "kk"
    LOGIN_EMAIL_GITHUB = "emgh"
    LOGIN_EMAIL_KAKAO = "emkk"
    LOGIN_GITHUB_KAKAO = "ghkk"
    LOGIN_EMAIL_GITHUB_KAKAO = "emghkk"
    LOGIN_CHOISES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "GitHub"), 
        (LOGIN_KAKAO, "Kakao"),
        (LOGIN_EMAIL_GITHUB, "Email+GitHub"),
        (LOGIN_GITHUB+LOGIN_KAKAO, "GitHub+Kakao"),
        (LOGIN_EMAIL_KAKAO, "Email+Kakao"),
        (LOGIN_EMAIL_GITHUB_KAKAO, "Email+GitHub+Kakao")
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)

    gender = models.CharField(_("gender"),choices=GENDER_CHOICES,
                              max_length=3, blank=True, default=GENDER_UNSPECIFIED)

    bio = models.TextField(_("bio"), blank=True)

    birthday = models.DateField(null=True, blank=True)

    language = models.CharField(
        choices=LANGUIGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_RUSSIAN)

    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_RUB)

    superhost = models.BooleanField(default=False)

    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=24, default="", blank=True)
    login_method = models.CharField(choices=LOGIN_CHOISES, max_length=6, default=LOGIN_EMAIL)

    def verify_email(self):
        if self.email_verified is False:
            while True:
                secret = uuid.uuid4().hex[:24]
                user = user_models.User.objects.filter(email_secret=secret)
                if len (user)==0:
                    self.email_secret = secret
                    break
            html_message = render_to_string("emails/verify_email.html", context={"secret": secret})
            send_mail(
                _("Verify airbnb-clone account"), 
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=True,
                html_message=html_message
                )

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'pk': self.pk})

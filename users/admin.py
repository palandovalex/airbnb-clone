from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms import models as room_models

# Register your models here.


class RoomInline(admin.TabularInline):
    model = room_models.Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """
    #list_filter = ("language", "currency", "superhost")

    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + ((
        "Custom profile",
        {"fields": (
            "avatar", "gender", "bio", "birthday", "language", "currency", "superhost", "email_verified", "email_secret", "login_method"
        )}
    ),)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "gender",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "login_method"
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

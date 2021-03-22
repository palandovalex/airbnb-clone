from django import forms
from django.forms import widgets

from django_countries.fields import CountryField

from . import models as room_models


class SearchForm(forms.Form):
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="RU").formfield()
    room_type = forms.ModelChoiceField(
        empty_label="Any kind", queryset=room_models.RoomType.objects.all(),
        required=False
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False, help_text="How many people will be staying?")
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        queryset=room_models.Amenity.objects.all(), required=False,
        widget= forms.CheckboxSelectMultiple
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=room_models.Facility.objects.all(), required=False,
        widget= forms.CheckboxSelectMultiple
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = room_models.Photo
        fields = ("caption", "file")

    def save(self, room, *args, **kwargs):
        photo = super().save(commit=False)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = room_models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
            "check_in",
            "check_out",
            "instant_book",
        )
        widgets = {
            "check_in": widgets.DateTimeInput(format="%Y-%m-%d %H:%M:%S"),
            "check_out": widgets.DateTimeInput(format="%Y-%m-%d %H:%M:%S"),
        }

    def save(self, user, * args, **kwargs):
        room = super().save(commit=False)
        room.host = user
        room.save()
        self.save_m2m()
        print(room.amenities)
        return room.pk
        

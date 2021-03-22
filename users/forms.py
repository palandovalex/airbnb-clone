from django import forms
from django.core.checks.messages import Error
from django.db import models
from django.forms import widgets
from . import models as user_models


class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}
    ))

    def clean(self):
        print("clean password")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = user_models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except user_models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User whith this email does not exist."))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = user_models.User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"})
        }

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    
    """def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user_models.User.objects.get(email=email)
            raise forms.ValidationError("User with this email already exists")
        except user_models.User.DoesNotExist:
            return email"""

    def clean_password(self):
        password: str = self.cleaned_data.get("password")
        if len(password)<=5:
            raise forms.ValidationError("Password is too short")

        if password != password.strip():
            raise forms.ValidationError("Password can not starts or ends by spaces")

        email = self.cleaned_data.get("email")
        if password == email:
            raise forms.ValidationError(
                "Password can not be equal to email.")

        return password

    def clean_password2(self):
        password: str = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords must be exactly equal")
        return password

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)
        user.username = email
        user.set_password(password)
        user.save()

        """first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        
        user = user_models.User.objects.create_user(email, email, password)

        user.first_name = first_name
        user.last_name = last_name
        user.save()"""

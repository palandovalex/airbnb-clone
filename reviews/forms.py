from django import forms
from . import models as review_models

class CreateReviewForm(forms.ModelForm):

    accuracy = forms.IntegerField(max_value=5, min_value=1)
    communication = forms.IntegerField(max_value=5, min_value=1)
    cleanlines = forms.IntegerField(max_value=5, min_value=1)
    location = forms.IntegerField(max_value=5, min_value=1)
    check_in = forms.IntegerField(max_value=5, min_value=1)
    value = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = review_models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanlines",
            "location",
            "check_in",
            "value",
        )

    def save(self):
       review = super().save(commit=False) # Call the real save() method
       return review

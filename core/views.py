from django.shortcuts import render
from django import forms

# Create your views here.



class MyDateInput(forms.DateInput):
    input_type = 'date'

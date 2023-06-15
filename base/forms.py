from .models import User
from django.forms import ModelForm
from django import forms

class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','phone','password','gender','country']

class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['gender','country','interests']


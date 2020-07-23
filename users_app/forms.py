from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from market.models import Customer


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerRegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['user']

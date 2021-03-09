from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ['user']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
	    model = User
	    fields = ['username', 'email']


from django import forms
import re
from pins.models import User
from django.core.exceptions import ObjectDoesNotExist


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Password',
                          widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='Password (Again)',
                        widget=forms.PasswordInput())

    def clean_password_confirmation(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password_confirmation = self.cleaned_data['password_confirmation']
            if password == password_confirmation:
                return password_confirmation
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Oops! Your username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('That username is already taken.')


class CreatePinForm(forms.Form):
    img_url = forms.CharField(
        label='Image URL',
        max_length=30,
        widget=forms.TextInput(attrs={
            'id':'img_url',
            'placeholder': 'Enter the image url',
        }))
    title = forms.CharField(
        label='Pin title',
        max_length=30,
        widget=forms.TextInput(attrs={
            'id':'title',
            'placeholder': 'Enter a pin title',
        }))
    description = forms.CharField(
        label='Pin description',
        widget=forms.TextInput(attrs={
            'id':'description',
            'placeholder': 'Describe your new pin',
        }))
    board_name = forms.CharField(
        label='Board name',
        max_length=30,
        widget=forms.TextInput(attrs={
            'id':'board_name',
            'placeholder': 'What board is your pin going in?',
        }))
    full_name = forms.CharField(
        label='Your full name',
        max_length=50,
        widget=forms.TextInput(attrs={
            'id':'full_name',
            'placeholder': 'Enter your full name'
        }))

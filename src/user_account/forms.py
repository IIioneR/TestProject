from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Form, fields
from django import forms

from user_account.models import User


class UserAccountRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'birth_date', 'image')


class UserAccountProfileForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image')


class ContactUs(Form):
    subject = fields.CharField(max_length=256, empty_value='Message from TMB')
    message = fields.CharField(widget=forms.Textarea)
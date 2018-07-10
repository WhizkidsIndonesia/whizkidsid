from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# test

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # remove username
        self.fields.pop('password2')

    class Meta:
        model = User
        fields = ('email', 'password1')
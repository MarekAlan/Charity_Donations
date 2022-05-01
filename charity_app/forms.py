from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'email'}),
                             label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
                               label="")


class CreateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    pass1 = forms.CharField(widget=forms.PasswordInput())
    pass2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = super().clean()
        if data['pass1'] != data['pass2']:
            raise ValidationError("Hasła się nie zgadzają")

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
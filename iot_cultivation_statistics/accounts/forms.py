# coding=utf-8
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, label=u'Nazwa użytkownika')
    password = forms.CharField(max_length=255, widget=forms.PasswordInput, label=u'Hasło')


class RegistrationForm(forms.Form):
    class Errors:
        EMAIL_ALREADY_USED = u'Podany adres e-mail jest zajęty'
        USERNAME_ALREADY_USED = u'Podana nazwa użytkownika jest już zajęta'
        CHARACTER_NOT_ALLOWED = u'W nazwie użytkownika nie może być znaku \'@\''

    email = forms.EmailField(max_length=255, label=u'Adres email')
    username = forms.CharField(max_length=255, label=u'Nazwa użytkownika')
    password = forms.CharField(max_length=255, min_length=4, widget=forms.PasswordInput, label=u'Hasło')
    first_name = forms.CharField(label=u'Imię', required=False)
    last_name = forms.CharField(label=u'Nazwisko', required=False)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': u'Wpisz adres email'})
        self.fields['username'].widget.attrs.update({'placeholder': u'Wpisz nazwę użytkownika'})
        self.fields['password'].widget.attrs.update({'placeholder': u'Podaj hasło'})
        self.fields['first_name'].widget.attrs.update({'placeholder': u'Podaj swoje imię'})
        self.fields['last_name'].widget.attrs.update({'placeholder': u'Podaj swoje nazwisko'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(RegistrationForm.Errors.EMAIL_ALREADY_USED)
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.find('@') != -1:
            raise forms.ValidationError(RegistrationForm.Errors.CHARACTER_NOT_ALLOWED)
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(RegistrationForm.Errors.USERNAME_ALREADY_USED)
        return username
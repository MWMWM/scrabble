#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from scrabble.models import User, UserProfile
from helper.views import Word

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=30, label="login")
    password = forms.CharField(max_length=32, label="hasło",
            error_messages={'required': 'musisz podać hasło'},
            widget=forms.PasswordInput)
    def clean_name(self):
        name = self.cleaned_data['name']
        if User.objects.filter(username=name).exists():
            raise forms.ValidationError("taki login już istnieje")
        return name

class LogForm(RegistrationForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if not User.objects.filter(username=name).exists():
            raise forms.ValidationError("taki login nie istnieje")
        return name
    def clean_password(self):
        name = self.cleaned_data['name']
        password = self.cleaned_data['password']
        if name and password:
            person = authenticate(username=name, password=password)
            if person is None:
                raise forms.ValidationError("podaj prawidłowe hasło")
        return password

class AccountForm(forms.Form):
    temp_password = forms.CharField(max_length=32, label="Aktualne hasło",
            widget=forms.PasswordInput)
    password = forms.CharField(max_length=32, label="Nowe hasło",
            widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, label="Potwierdź nowe hasło",
            widget=forms.PasswordInput)
    def __init__(self, user=None, data=None):
        super(AccountForm, self).__init__(data=data)
        self.user = user
    def clean_temp_password(self):
        temp_password = self.cleaned_data['temp_password']
        if not self.user.check_password(temp_password):
            raise forms.ValidationError("Hasło nie zgadza się z Twoim hasłem")
        return temp_password
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Hasło nie zgadza się z powyższym")
        return password2

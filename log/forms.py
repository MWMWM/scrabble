#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from scrabble.models import User, UserProfile
from helper.views import Word

class LogForm(forms.Form):
    name = forms.CharField(max_length=30, label="login")
    password = forms.CharField(max_length=32, label="hasło", 
            error_messages={'required': 'musisz podać hasło'},
            widget=forms.PasswordInput)
    def clean_name(self):
       name = self.cleaned_data['name']
       if not User.objects.filter(username = name).exists():
           raise forms.ValidationError("taki login nie istnieje")
       return name
    def clean(self):
       cleaned_data = super(LogForm, self).clean()
       name = cleaned_data.get('name')
       password = cleaned_data.get('password')
       if name and password:
           person = authenticate(username = name, password = password)
           if person is None:
               raise forms.ValidationError("podaj prawidłowe hasło")
       return cleaned_data

class RegistrationForm(LogForm):
    def clean_name(self):
       name = self.cleaned_data['name']
       if User.objects.filter(username = name).exists():
           raise forms.ValidationError("taki login już istnieje")
       return name
    def clean(self):
       cleaned_data = super(LogForm, self).clean()
       return cleaned_data

#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from log.models import User, UserProfile

class LoggingForm(forms.Form):
    name = forms.CharField(max_length=30, label="login")
    password = forms.CharField(max_length=32, label="hasło", 
        #    error_messages={'required': 'musisz podać hasło'},
            widget=forms.PasswordInput)
    def clean_name(self):
       name = self.cleaned_data['name']
       if not User.objects.filter(username = name).exists():
           raise forms.ValidationError("taki login nie istnieje")
       return name

class RegistrationForm(LoggingForm):
    language = forms.CharField(max_length=2, label="język", 
            widget=forms.Select(choices=UserProfile.lang_choices))
    def clean_name(self):
       name = self.cleaned_data['name']
       if User.objects.filter(username = name).exists():
           raise forms.ValidationError("taki login już istnieje")
       return name


#!/usr/bin/python
# -*- coding: utf-8 -*-

from helper.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from scrabble.views import RenderWithInf
from log.forms import LoggingForm, RegistrationForm

def Login(request, where):
    if request.POST:
        form = LoggingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            person = authenticate(username = name, password = password)
            if person is not None:
                login(request, person)
                return HttpResponseRedirect(where)
    else:
        form = LoggingForm()
    return RenderWithInf('log/login.html', request, {'form': form})

def Register(request, where):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            if not User.objects.filter(username = name):
                User.objects.create_user(username = name, password = password)
            else:
                messages.error(request, 'konto o takim loginie już istnieje')
            person = authenticate(username = name, password = password)
            if person is not None:
                login(request, person)
                return HttpResponseRedirect(where)
    else:
        form = RegistrationForm()
    return RenderWithInf('log/register.html', request, {'form': form})


def Logout(request, where):
    logout(request)
    return HttpResponseRedirect(where)

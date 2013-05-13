#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from scrabble.views import RenderWithInf
from scrabble.models import User, UserProfile
from log.forms import LogForm, RegistrationForm, AccountForm

def Login(request, where):
    if request.POST:
        form = LogForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            person = authenticate(username = name, password = password)
            if person is not None:
                login(request, person)
                where = where.replace('Register/', '')
                return HttpResponseRedirect(where)
    else:
        form = LogForm()
    return RenderWithInf('log/login.html', request, {'form': form})

def Register(request, where):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            if not User.objects.filter(username = name):
                user = User.objects.create_user(username = name, 
                        password = password)
                UserProfile.objects.create(user = user)
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

def AccountSettings(request):
    if request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
           form.save()
    else:
        form = AccountForm()
    print form
    return RenderWithInf('log/account_settings.html', request, {'form': form})

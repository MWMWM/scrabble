#!/usr/bin/python
# -*- coding: utf-8 -*-

from helper.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from scrabble.views import RenderWithInf

def Login(request, where):
    if request.POST:
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        if 'addlog' in request.POST:
            if not User.objects.filter(username = name):
                User.objects.create_user(username = name, password = password)
        person = authenticate(username = name, password = password)
        if person is not None:
            login(request, person)
            return HttpResponseRedirect(where)
        else:
            messages.error(request, 'Błąd: podano nieprawidłowe dane')
            if User.objects.filter(username = name):
                messages.error(request, 'taki login istnieje, \
                        ale hasło nie odpowiada temu kontu')
            else:
                messages.error(request, 'taki login nie istnieje')
    return RenderWithInf('log/login.html', request)

def Logout(request, where):
    logout(request)
    return HttpResponseRedirect(where)

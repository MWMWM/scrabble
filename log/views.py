#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from scrabble.models import User, UserProfile
from log.forms import LogForm, RegistrationForm, AccountForm

def Login(request, where):
    if request.POST:
        form = LogForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            person = authenticate(username=name, password=password)
            if person is not None:
                login(request, person)
                where = where.replace('Register/', '')
                return HttpResponseRedirect(where)
    else:
        form = LogForm()
    return render_to_response('log/login.html', {'form': form},
            context_instance=RequestContext(request))

def Register(request, where):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            if not User.objects.filter(username=name):
                user = User.objects.create_user(username=name,
                        password=password)
                UserProfile.objects.create(user=user)
            else:
                messages.error(request, 'konto o takim loginie już istnieje')
            person = authenticate(username=name, password=password)
            if person is not None:
                login(request, person)
                return HttpResponseRedirect(where)
    else:
        form = RegistrationForm()
    return render_to_response('log/register.html', {'form': form},
            context_instance=RequestContext(request))

def Logout(request, where):
    logout(request)
    return HttpResponseRedirect(where)

def AccountSettings(request, username):
    if request.user.username == username:
        if request.POST:
            form = AccountForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = User.objects.get(username=username)
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.info(request, "Twoje hasło zostało zmienione")
        else:
            form = AccountForm(user=request.user)
    else:
        messages.error(request, "Nie masz prawa edytować tamtej strony")
        return HttpResponseRedirect(reverse('home'))
    return render_to_response('log/account_settings.html', {'form': form},
            context_instance=RequestContext(request))

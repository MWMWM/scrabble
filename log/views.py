#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import simplejson
from scrabble.models import User, UserProfile, Word
from log.forms import LogForm, RegistrationForm, AccountForm


def Login(request, where=''):
    if request.POST:
        form = LogForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            person = authenticate(username=name, password=password)
            if person is not None:
                login(request, person)
                if not where:
                    where = request.REQUEST.get('next', '')
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
            user = User.objects.create_user(username=name, password=password)
            UserProfile.objects.create(user=user)
            person = authenticate(username=name, password=password)
            if person is not None:
                login(request, person)
                return HttpResponseRedirect(where)
    else:
        form = RegistrationForm()
    return render_to_response('log/register.html', {'form': form},
            context_instance=RequestContext(request))


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def AccountSettings(request):
    if request.POST:
        form = AccountForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.info(request, "Twoje hasło zostało zmienione")
    else:
        form = AccountForm(user=request.user)
    return render_to_response('log/account_settings.html', {'form': form},
            context_instance=RequestContext(request))


def DeleteAccount(request):
    who = request.user
    Word.objects.filter(added_by=who).delete()
    logout(request)
    UserProfile.objects.get(user=who).delete()
    who.delete()
    return HttpResponseRedirect(reverse('home'))


def CheckAvailability(request):
    name = request.POST.get('name', None)
    is_availeable = False
    error = False
    if name:
        if not User.objects.filter(username=name).exists():
            is_availeable = True
    else:
        error = True
    return HttpResponse(simplejson.dumps({
            'is_availeable': is_availeable, 'error': error}),
        mimetype='application/jvascript')

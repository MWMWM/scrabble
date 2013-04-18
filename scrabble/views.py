#!/usr/bin/python
# -*- coding: utf-8 -*-

from helper.models import Word, User
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def RenderWithInf(template, request, args={}):
    words_number = Word.objects.distinct().count()
    if words_number ==1:
        messages.info(request, 'w bazie jest obecnie ' + str(words_number) + ' słowo')
    if 0 < words_number < 5:
        messages.info(request, 'w bazie są obecnie ' + str(words_number) + ' słowa')
    else:
        messages.info(request, 'w bazie jest obecnie ' + str(words_number) + ' słów')
    user = request.user
    if not user.username:
        messages.info(request, 'nie jesteś zalogowany')
    else:
        messages.info(request, u'jesteś zalogowany jako: ' + user.username)
    return render_to_response (template, args, 
            context_instance=RequestContext(request))

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
    return RenderWithInf('scrabble/login.html', request)

def Logout(request, where):
    logout(request)
    return HttpResponseRedirect(where)

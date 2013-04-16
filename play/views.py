#!/usr/bin/python
# -*- coding: utf-8 -*-

from string import ascii_lowercase
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from helper.models import Word, User
from scrabble.views import RenderWithInf

def Main(request, letters, result=0):
    board = ''
    if 'check' in request.POST:
        result = int(result)
        word = request.POST.get('word','')
        if word in letters:
            result += AddPoints(word)
            for letter in len(word):
                string.replace(letters, letter, NewLetter())
        return HttpResponseRedirect(reverse('play:main3', args=(letters, result )))
    return RenderWithInf('play/main.html', request, {
        'letters': letters, 'board': board, 'result':result})

def NewLetters(request):
    letters = "".join(NewLetter() for i in range(6))
    return  HttpResponseRedirect(reverse('play:main'))

def NewLetter():
    letters = random.choice(ascii_lowercase) # + u'ęóąśłżźćń')
    return letters

def AddPoints(word):
    return len(word)

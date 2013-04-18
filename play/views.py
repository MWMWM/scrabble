#!/usr/bin/python
# -*- coding: utf-8 -*-
import string
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from helper.models import Word, User
from scrabble.views import RenderWithInf

def Main(request):
    result = 0
    letters = "".join(NewLetter() for i in range(6))
    return HttpResponseRedirect(reverse('play:playing', 
        kwargs={'letters': letters, 'result': result}))

def Playing(request, letters, result):
    board = NewBoard()
    print request.POST
    if 'check' in request.POST:
        result = int(result)
        word = request.POST.get('word','')
        print word
        if word in letters: # poprawić
            result += AddPoints(word)
            for letter in word:
                string.replace(letters, letter, NewLetter())
        else:
            messages.error(request, 'nie możesz utworzyć tego słowa')
        print letters
        print result
        return HttpResponseRedirect(reverse('play:playing', 
             kwargs={'letters': letters, 'result': result}))
    return RenderWithInf('play/main.html', request, {
        'letters': letters, 'board': board, 'result':result})

def NewLetters(request):
    letters = "".join(NewLetter() for i in range(6))
    return  HttpResponseRedirect(reverse('play:main'))

def NewLetter():
    letters = random.choice(string.ascii_lowercase) # + u'ęóąśłżźćń')
    return letters

def AddPoints(word):
    return len(word)

def NewBoard():
    return ''

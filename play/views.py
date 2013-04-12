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

def Main(request, result=0):
    letters = u'abć'
    board = ''
    if 'check' in request.POST:
        word = request.POST.get('word','')
        result += len(word)
    return RenderWithInf('play/main.html', request, {
        'letters': letters, 'board': board, 'result':result})

def NewLetters(request):
    letters = random.choice(ascii_lowercase + u'ęóąśłżźćń')
    print letters
    return HttpResponseRedirect(reverse('p_main'))

def Create(request):
    if request.method =='POST':
        return  HttpResponseRedirect(reverse('h_main'))

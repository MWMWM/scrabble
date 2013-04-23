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
from helper.views import Code
from helper.models import Word

def Main(request):
    result = 0
    letters = "".join(NewLetter() for i in range(8))
    return HttpResponseRedirect(reverse('play:playing', 
        kwargs={'result': result, 'letters': letters}))

def Playing(request, letters, result):
    if 'check' in request.POST:
        result = int(result)
        word = request.POST.get('word','')
        if Word.objects.filter(word=word).exists():
            for letter in word:
                if letter in letters:
                    letters.replace(letter, "", 1)
                else:
                    messages.error(request, 'nie możesz utworzyć tego słowa - \
                            nie masz odpowiednich literek')
                    return RenderWithInf('play/main.html', request, {
                        'letters': letters, 'result':result})
            for letter in word:
                letters = letters.join(NewLetter())
            result += AddPoints(word)
        else:
            messages.error(request, 'nie możesz utworzyć tego słowa - \
                    nie ma go w słowniku')
        return HttpResponseRedirect(reverse('play:playing', kwargs={
            'letters': letters, 'result': result}))
    return RenderWithInf('play/main.html', request, {
        'letters': letters, 'result':result})

def NewLetters(request, result):
    letters = "".join(NewLetter() for i in range(8))
    if Word.objects.filter(code = Code(letters)).exists():
        if result > 10:
            result = int(result) - 10
            messages.info(request, 'można było ułożyć słowo')
        else:
            messages.info(request, 'koniec gry - uzyskano ujemną liczbę punktów')
            return HttpResponseRedirect(reverse('play:main'))
    return  HttpResponseRedirect(reverse('play:playing', 
        kwargs={'result': result, 'letters': letters}))

def NewLetter():
    #letters = string.ascii_lowercase
    letters = u'abcdefghijklmnopqrstuvwxyzęóąśłżźćń'
    letter = random.choice(letters)
    return letter

def AddPoints(word):
    return len(word)


#!/usr/bin/python
# -*- coding: utf-8 -*-
import string
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse

from helper.models import Word, User
from scrabble.views import RenderWithInf
from helper.views import Code, AddWord

def Playing(request, letters, result=0):
    if 'check' in request.POST:
        result = int(result)
        word = request.POST.get('word','')
        if Word.objects.filter(word=word).exists():
            if set(word).issubset(set(letters)):
                for letter in word:
                    letters = letters.replace(letter, NewLetter(), 1)
                result += AddPoints(word)
                return HttpResponseRedirect(reverse('play:playing', kwargs={
                    'letters': letters, 'result': result}))
            else:
                messages.error(request, 'nie możesz utworzyć tego słowa - \
                        nie masz odpowiednich literek')
        else:
             return RenderWithInf('play/main.html', request, {
                'letters': letters, 'result':result, 'word': word})
    return RenderWithInf('play/main.html', request, {
        'letters': letters, 'result':result})

def ChangeLetters(request, result):
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
    letters = u'abcdefghijklmnoprstuwyzęóąśłżźćń'
    return random.choice(letters)

def NewLetters():
    return "".join(NewLetter() for i in range(8))

def AddPoints(word):
    return len(word)


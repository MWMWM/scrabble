#!/usr/bin/python
# -*- coding: utf-8 -*-
import string
import random
from collections import Counter
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from scrabble.models import Word, User
from scrabble.views import RenderWithInf
from helper.views import Code, AddWord

def Main(request):
    all_letters = NewLetters('pl')
    return HttpResponseRedirect(reverse('playing', kwargs={
        'result': 0, 'all_letters': all_letters, 'temp_letters': ""}))

def Playing(request, result, all_letters, temp_letters):
    left_letters = list((Counter(all_letters) - Counter(temp_letters)).elements())
    language = request.session.get('language', 'pl')
    if not Word.objects.filter(word=temp_letters, language = language).exists():
        to_add = True
    else:
        to_add = False
    if 'check' in request.POST:
        result = int(result)
        if Word.objects.filter(word=temp_letters, language = language).exists():
            for letter in temp_letters:
                all_letters = all_letters.replace(letter, NewLetter(language),1)
            w = Word.objects.get(word = temp_letters, language = language)
            result += w.points 
            return HttpResponseRedirect(reverse('playing', kwargs={
                'all_letters': all_letters, 'temp_letters': "",
                'result': result}))
    return RenderWithInf('play/main.html', request, {'result':result, 
        'all_letters': all_letters, 'left_letters': left_letters, 
        'temp_letters': temp_letters, 'to_add': to_add})

def ChangeLetters(request, result, letters):
    if Word.objects.filter(code = Code(letters)).exists():
        if result > 10:
            result = int(result) - 10
            messages.info(request, 'można było ułożyć słowo ze wszystkich literek')
        else:
            messages.info(request, 'koniec gry - uzyskano ujemną liczbę punktów')
            return HttpResponseRedirect(reverse('play'))
    language = request.session.get('lang', 'pl')
    letters = "".join(NewLetter(language) for i in range(8))
    return  HttpResponseRedirect(reverse('playing', 
        kwargs={'result': result, 'all_letters': letters, 'temp_letters': "" }))

def NewLetter(language):
    if language == 'pl':
        letters = u'abcdefghijklmnoprstuwyzęóąśłżźćń'
    elif language == 'en':
        letters = string.ascii_lowercase
    return random.choice(letters)

def NewLetters(language):
    return "".join(NewLetter(language) for i in range(8))

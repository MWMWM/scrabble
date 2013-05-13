#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from collections import Counter
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from scrabble.models import Word, User, Language
from scrabble.views import RenderWithInf
from helper.views import Code, AddWord

def Main(request):
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    all_letters = "".join(NewLetter(language) for i in range(8))
    return HttpResponseRedirect(reverse('playing', kwargs={
        'result': 0, 'all_letters': all_letters, 'temp_letters': ""}))

def Playing(request, result, all_letters, temp_letters):
    left_letters = list((Counter(all_letters) - Counter(temp_letters)).elements())
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    if not Word.objects.filter(word=temp_letters, language = language).exists():
        to_add = True
    else:
        to_add = False
        if 'check' in request.POST:
            result = int(result)
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
    language = request.session.get('lang', 'pl')
    language = Language.objects.get(short=language)
    if Word.objects.filter(code = Code(letters), language = language).exists():
        if result > 10:
            result = int(result) - 10
            messages.info(request, 'Można było ułożyć słowo ze wszystkich literek')
        else:
            messages.info(request, 'Koniec gry - uzyskano ujemną liczbę punktów')
            return HttpResponseRedirect(reverse('play'))
        letters = "".join(NewLetter(language) for i in range(8))
    return  HttpResponseRedirect(reverse('playing', 
        kwargs={'result': result, 'all_letters': letters, 'temp_letters': "" }))

def Delete(request, result, all_letters, temp_letters, letter=''):
    temp_letters = temp_letters.replace(letter, '', 1)
    return HttpResponseRedirect(reverse('playing', kwargs={'result':result, 
        'all_letters': all_letters, 'temp_letters': temp_letters}))

def NewLetter(language):
    return random.choice(language.letters)


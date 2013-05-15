#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from collections import Counter
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from scrabble.models import Word, User, Language, UserProfile
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
            player = UserProfile.objects.get(user = request.user)
            if player.best_score < result:
                player.best_score = result
                player.save()
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

def Delete(request, where, temp_letters, letter=''):
    temp_letters = temp_letters.replace(letter, '', 1)
    return HttpResponseRedirect('/' + where + '/' + temp_letters)

def Guess(request, result=0, guesses=0, all_letters='', temp_letters=''):
    left_letters = list((Counter(all_letters) - Counter(temp_letters)).elements())
    if not left_letters:
        if all_letters:
            language = request.session.get('language', 'pl')
            language = Language.objects.get(short=language)
            guesses = int(guesses) + 1
            if Word.objects.filter(word = temp_letters, language = language).exists():
                result = int(result) + 1
                messages.info(request, "Utworzony wyraz był poprawny")
            else:
                word = Word.objects.filter(word = all_letters, language = language)[0]
                messages.info(request, u"Utworzony wyraz nie był poprawny, \
                        można było utworzyć <{}>".format(word))
        all_letters = random.choice(Word.objects.all())
        return HttpResponseRedirect(reverse('guessed', kwargs={
            'result': result, 'guesses': guesses, 'all_letters': all_letters}))
    return RenderWithInf('play/guess.html', request, {'result': result, 
        'guesses': guesses, 'temp_letters': temp_letters, 'left_letters': left_letters})

def NewLetter(language):
    return random.choice(language.letters)


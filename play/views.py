#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from collections import Counter
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from scrabble.models import Word, User, Language, UserProfile, NewLetters
from scrabble.views import RenderWithInf
from helper.views import Code, AddWord, CheckSubwords

def StartPlay(request):
    player = UserProfile.objects.get(user = request.user)
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    player.prepare_for_play(language)
    return RenderWithInf('play/main.html', request, {
        'left_letters': player.last_all_letters, 'player': player})

def Play(request):
    player = UserProfile.objects.get(user = request.user)
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    left_letters = list((Counter(player.last_all_letters) - Counter(
            player.last_temp_letters)).elements())
    if not Word.objects.filter(word=player.last_temp_letters, language=language).exists():
        to_add = True
        if 'check' in request.POST:
            messages.error(request, "Tego słowa nie ma przecież w słowniku")
    else:
        to_add = False
        if 'check' in request.POST:
            w = Word.objects.filter(word = player.last_temp_letters, language = language)      
            player.last_score += w[0].points
            left_letters += NewLetters(language, len(player.last_temp_letters))
            player.last_temp_letters = ''
            player.last_all_letters = ''.join(left_letters)
            player.save()
    return RenderWithInf('play/main.html', request, {'left_letters': left_letters, 
        'to_add': to_add, 'player': player})

def AddLetter(request, letter):
    player = UserProfile.objects.get(user = request.user)
    player.last_temp_letters += letter
    player.save()
    return HttpResponseRedirect(reverse('play'))

def DeleteLetter(request, letter):
    player = UserProfile.objects.get(user = request.user)
    player.last_temp_letters = player.last_temp_letters.replace(letter, '', 1)
    player.save()
    return HttpResponseRedirect(reverse('play'))

def ChangeLetters(request):
    player = UserProfile.objects.get(user = request.user)
    language = request.session.get('lang', 'pl')
    language = Language.objects.get(short=language)
    words = CheckSubwords(player.last_all_letters, language)
    if words:
        if len(words) == 1:
            player.last_score -= 5
            messages.info(request, u'Można było ułożyć słowo <{}> i dlatego \
                    odjęto Ci 5 punktów'.format(words[0]))
        else:
            player.last_score -= 10
            print len(words)
            messages.info(request, u'Można było ułożyć takie słowa, jak: <{}> \
                    i dlatego odjęto Ci 10 punktów'.format(
                            '>, <'.join(w.word for w in words)))
    player.last_all_letters = "".join(NewLetters(language, 8))
    player.last_temp_letters = ""
    player.save()
    return  HttpResponseRedirect(reverse('play'))

def Delete(request, where, temp_letters, letter=''):
    temp_letters = temp_letters.replace(letter, '', 1)
    return HttpResponseRedirect('/' + where + '/' + temp_letters)

def Guess(request, result=0, guesses=0, all_letters='', temp_letters=''):
    left_letters = list((Counter(all_letters) - Counter(temp_letters)).elements())
    if not left_letters:
        language = request.session.get('language', 'pl')
        language = Language.objects.get(short=language)
        if all_letters:
            guesses = int(guesses) + 1
            if Word.objects.filter(word = temp_letters, language = language).exists():
                result = int(result) + 1
                messages.info(request, "Utworzony wyraz był poprawny")
            else:
                word = Word.objects.filter(word = all_letters, language = language)
                messages.info(request, u"Utworzony wyraz nie był poprawny, można\
                        było utworzyć <{}>".format('>, <'.join(w.word for w in word)))
        all_letters = random.choice(Word.objects.filter(language = language))
        return HttpResponseRedirect(reverse('guessed', kwargs={
            'result': result, 'guesses': guesses, 'all_letters': all_letters}))
    return RenderWithInf('play/guess.html', request, {'result': result, 
        'guesses': guesses, 'temp_letters': temp_letters, 'left_letters': left_letters})


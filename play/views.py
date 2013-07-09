#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import random
from collections import Counter
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.utils import simplejson
from scrabble.models import Word, UserProfile, Language, UserProfile, NewLetters
from helper.views import Code, AddWord, CheckSubwords


def ChoseForm(nb, option_less, option_more):
    if nb > 4:
        return str(nb) + ' ' + option_more
    return str(nb) + option_less


def Play(request):
    player = UserProfile.objects.get(user=request.user)
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    if not set(player.last_all_letters).issubset(language.letters):
        player.prepare_for_play(language)
    left_letters = list((Counter(player.last_all_letters) - Counter(
        player.last_temp_letters)).elements())
    return render_to_response('play/main.html', {'left_letters': left_letters,
        'player': player}, context_instance=RequestContext(request))


def StartPlay(request):
    player = UserProfile.objects.get(user=request.user)
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    player.prepare_for_play(language)
    return HttpResponseRedirect(reverse('play'))


def Check(request):
    player = UserProfile.objects.get(user=request.user)
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    left_letters = list((Counter(player.last_all_letters) - Counter(
        player.last_temp_letters)).elements())
    try:
        w = Word.objects.get(word=player.last_temp_letters, language=language)
        messages.info(request, TellTheBest(player.last_all_letters, language))
        player.last_score += w.points
        messages.info(request, u'Dodano Ci {}'.format(ChoseForm(
            w.points, 'punkty', u'punktów')))
        left_letters += NewLetters(language, len(player.last_temp_letters))
        player.last_temp_letters = ''
        player.last_all_letters = ''.join(left_letters)
        player.save()
    except (DatabaseError, ObjectDoesNotExist):
        return render_to_response('play/main.html', {'not_existing': True,
           'left_letters': left_letters, 'player': player},
           context_instance=RequestContext(request))
    return  HttpResponseRedirect(reverse('play'))


def TellTheBest(letters, language):
    for_regex = '^' + r'?'.join(Code(letters)) + '?$'
    try:
        word = Word.objects.filter(code__regex=for_regex,
                language=language).order_by('-points')[0]
    except IndexError:
        return u'Nie można ułożyć żadnego słowa'
    return u'Najlepsze słowo, jakie można było ułożyć, to {} za {}'.format(
            word.word, ChoseForm(word.points, 'punkty', u'punktów'))


def AddLetter(request, letter):
    player = UserProfile.objects.get(user=request.user)
    player.last_temp_letters += letter
    player.save()
    return HttpResponseRedirect(reverse('play'))


def DeleteLetter(request, letter):
    player = UserProfile.objects.get(user=request.user)
    player.last_temp_letters = player.last_temp_letters.replace(letter, '', 1)
    player.save()
    return HttpResponseRedirect(reverse('play'))


def ChangeLetters(request):
    player = UserProfile.objects.get(user=request.user)
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    words = CheckSubwords(player.last_all_letters, language)
    if words:
        if len(words) == 1:
            player.last_score -= 5
            messages.info(request, u'Można było ułożyć słowo <{}> i dlatego \
                    odjęto Ci 5 punktów'.format(words[0]))
        else:
            player.last_score -= 10
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


def Guess(request):
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    letters = Word.objects.filter(language=language).order_by('?')[0].word
    request.session['last_letters'] = letters
    return render_to_response('play/guess.html', {'letters': letters,
        'result': 0, 'guesses': 0}, context_instance=RequestContext(request))


def CheckGuess(request):
    regex = request.GET.get('regex', None)
    letters = request.session.get('last_letters', None)
    regex = re.split('&letter\[\]=', regex)
    regex[0] = regex[0].replace('letter[]=', '')
    word = ''
    for nb, letter in enumerate(letters):
        word += letters[int(regex[nb]) - 1]
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    if Word.objects.filter(word=word, language=language).exists():
        was_correct = True
        possible_words = ''
    else:
        words = Word.objects.filter(code=Code(word), language=language)
        possible_words = ''
        for word in words:
            possible_words += word.word + ' '
        was_correct = False
    letters = Word.objects.filter(language=language).order_by('?')[0].word
    request.session['last_letters'] = letters
    return HttpResponse(simplejson.dumps({'letters': letters,
        'was_correct': was_correct, 'possible_words': possible_words}),
        mimetype='application/jvascript')

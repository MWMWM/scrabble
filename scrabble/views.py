#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from scrabble.models import Word, Language, User, UserProfile


def MyContextProcessor(request):
    lang = request.session.get('language', 'pl')
    return {'user':request.user,
            'lang': Language.objects.get(short=lang),
            'languages': Language.objects.exclude(short=lang)}


def ChangeLang(request, lang, where):
    request.session['language'] = lang
    if 'play_' in where:
        player = UserProfile.objects.get(user=request.user)
        language = Language.objects.get(short=lang)
        player.prepare_for_play(language)
    if 'guess' in where:
        is_guess = True
    else:
        is_guess = False
    json = simplejson.dumps(is_guess)
    return HttpResponse(json, mimetype='application/json')


def Home(request):
    words_number = Word.objects.distinct().count()
    if words_number == 1:
        messages.info(request, 'W bazie jest obecnie ' + str(words_number) + \
                ' słowo')
    elif 1 < words_number % 10 < 5 and words_number < 1000:
        messages.info(request, 'W bazie są obecnie ' + str(words_number) + \
                ' słowa')
    else:
        messages.info(request, 'W bazie jest obecnie ' + str(words_number) + \
                ' słów')
    users = User.objects.all()
    return render_to_response('scrabble/home.html', {'users': users},
            context_instance=RequestContext(request))

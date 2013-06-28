#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.http import HttpResponse
from scrabble.models import Word, Language, User

def MyContextProcessor(request):
    return {'user':request.user, 
            'lang': request.session.get('language', 'pl'),
            'languages': Language.objects.all()}

def ChangeLang(request, lang):
    request.session['language'] = lang
    return HttpResponse()

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

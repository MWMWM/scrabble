#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrabble.models import Word, Language
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

def RenderWithInf(template, request, args={}):
    args['user'] = request.user.username
    args['lang'] = request.session.get('language', 'pl')
    args['languages'] = Language.objects.all()
    return render_to_response (template, args, 
            context_instance=RequestContext(request))

def ChangeLang(request, lang):
    request.session['language'] = lang
    return HttpResponse()

def Home(request):
    words_number = Word.objects.distinct().count()
    if words_number ==1:
        messages.info(request, 'W bazie jest obecnie ' + str(words_number) + \
                ' słowo')
    elif 1 < words_number % 10 < 5:
        messages.info(request, 'W bazie są obecnie ' + str(words_number) + \
                ' słowa')
    else:
        messages.info(request, 'W bazie jest obecnie ' + str(words_number) + \
                ' słów')
    return RenderWithInf('base.html', request)

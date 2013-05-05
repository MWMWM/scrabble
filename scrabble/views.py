#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrabble.models import Word
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.http import HttpResponse
def RenderWithInf(template, request, args={}):
    words_number = Word.objects.distinct().count()
    if words_number ==1:
        messages.info(request, 'w bazie jest obecnie ' + str(words_number) + \
                ' słowo')
    elif 1 < words_number < 5:
        messages.info(request, 'w bazie są obecnie ' + str(words_number) + \
                ' słowa')
    else:
        messages.info(request, 'w bazie jest obecnie ' + str(words_number) + \
                ' słów')
    user = request.user
    if not user.username:
        messages.info(request, 'nie jesteś zalogowany')
    else:
        messages.info(request, u'jesteś zalogowany jako: ' + user.username)
    if user.username:
        args['lang'] = request.user.userprofile.language
    elif request.COOKIES.has_key('lang'):
        args['lang'] = request.COOKIES['lang']
    else:
        args['lang'] = 'pl'
        response = HttpResponse()
        response.set_cookie('lang', 'pl')
    return render_to_response (template, args, 
            context_instance=RequestContext(request))


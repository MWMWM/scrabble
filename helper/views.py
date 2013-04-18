#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools, urllib, re, string
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from helper.models import Word, User
from scrabble.views import RenderWithInf

def Main(request):
    if 'find' in request.POST:
        where = request.POST.get('where', '')
        word = request.POST.get('word_to_check', '')
        direction = '/help/' + where + '/' + word
        return HttpResponseRedirect(direction)
    if 'add' in request.POST:
        if not request.user.username:
            messages.error(request, 'by dodać jakiekolwiek słowo musisz być zalogowany')
        else:
            where = request.POST.get('howmany', '')
            if where == 'AddMultiple':
                AddWords(request)
            elif where == 'AddOne':
                AddWord(request)
    return RenderWithInf('helper/main.html', request)

def AddWord(request):
    word = request.POST.get('word_to_add', '')
    if AddOne(word, request.user):
        messages.info(request, u'Dodano wyraz <{}>'.format(word))
    else:
        messages.info(request, u'Słowo <{}> jest już w Twojej bazie'.format(word))

def AddWords(request):
    file = request.FILES['plik']
    if file:
        text = file.read()
        how_many = 0
        for word in re.split('[\s,?!;:()-]', text):
            if re.search('[."\']', word) == None:
                how_many += AddOne(word.decode('utf-8'), request.user)
        if how_many == 1:
            messages.ifo(request, 'dodano słowo')
        if 1 < how_many < 5:
            messages.ifo(request, 'dodano' + str(how_many) + ' słowa')
        else:
            messages.info(request, 'dodano ' + str(how_many) + ' słów')
    else:
        messages.error(request, 'nie wybrano pliku do dodania')

def XxResult(request, xx, word):
    letters = string.ascii_lowercase + u'ęóąśłżźćń'
    if '*' in word:
        existing_words = []
        for letter in letters:
            if xx == 'my':
                existing_words.extend(Word.objects.filter(
                    code = Code(word.replace('*', letter)), 
                    added_by = request.user))
            else:
                existing_words.extend(Word.objects.filter(
                    code = Code(word.replace('*', letter))))
    else:
        if xx == 'my':
            existing_words = Word.objects.filter(code = Code(word), 
                added_by = request.user)
        else:
            existing_words = Word.objects.filter(code = Code(word))
    return RenderWithInf('helper/results.html', request, {
        'words': existing_words, 'whose': 'all'})

def Delete(request, where, word):
    print where
    if request.user.username:
        word_to_delete = Word.objects.get(word = word, added_by = request.user)
        if word_to_delete.added_by.count() > 1:
            word_to_delete.added_by.remove(request.user)
        else:
            word_to_delete.delete()
    else:
        messages.errors(request, 'nie możesz usunąć słowa, które nie należy do Ciebie')
    return HttpResponseRedirect('/help/' + where)

def AddOne(word, added_by):
    if word == word.lower() and 1 < len(word) < 9:
        word, created = Word.objects.get_or_create(word = word, code = Code(word))
        if not Word.objects.filter(word = word, added_by = added_by).exists(): 
            word.added_by.add(added_by)
            return 1
    return 0

def Code(word):
    return ''.join(sorted(word[:]))


#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools, urllib, re
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from scrabble.models import Word, User
from scrabble.views import RenderWithInf
from helper.forms import AddForm

def AddPage(request):
    if request.POST:
        form = AddForm(request.POST, request.FILES)
        if not request.user.username:
            messages.error(request, 'by dodać jakiekolwiek słowo \
                    musisz być zalogowany')
        elif form.is_valid(): 
            words = form.cleaned_data['words']
            wordsfile = form.cleaned_data['wordsfile']
            if words:
                AddWords(words, request)
            if wordsfile:
                file = request.FILES['wordsfile']
                if file:
                    AddWords(file.read(), request)
                else:
                    messages.error(request, 'nie wybrano pliku do dodania')
    else:
        form = AddForm()
    return RenderWithInf('helper/add.html', request, {'form': form})

def FindPage(request):
    if 'find' in request.POST:
        where = request.POST.get('where', '')
        word = request.POST.get('word_to_check', '')
        return HttpResponseRedirect(reverse('help:xxresult', kwargs={
            'where':where, 'word':word}))
    return RenderWithInf('helper/find.html', request)

def AddWord(request, word, where):
    if request.user.username:
        if AddOne(word, request.user):
            messages.info(request, u'Dodano wyraz <{}>'.format(word))
    else:
        messages.error(request, 'by dodać jakiekolwiek słowo musisz być zalogowany')
    return HttpResponseRedirect(where)

def AddWords(text, request):
    how_many = 0
    for word in re.split('[\s,?!;:()-]', text):
        if re.search('[."\']', word) == None:
            how_many += AddOne(word.decode('utf-8'), request.user)
    if how_many == 1:
        messages.info(request, 'dodano słowo')
    elif 1 < how_many < 5:
        messages.info(request, 'dodano ' + str(how_many) + ' słowa')
    else:
        messages.info(request, 'dodano ' + str(how_many) + ' słów')
    
def XxResult(request, where, word):
    letters = u'abcdefghijklmnoprstuwyzęóąśłżźćń'
    if '*' in word:
        existing_words = []
        for letter in letters:
            if where == 'MyResult':
                existing_words.extend(Word.objects.filter(
                    code = Code(word.replace('*', letter)), 
                    added_by = request.user))
            else:
                existing_words.extend(Word.objects.filter(
                    code = Code(word.replace('*', letter))))
    else:
        if where == 'MyResult':
            existing_words = Word.objects.filter(code = Code(word), 
                added_by = request.user)
        else:
            existing_words = Word.objects.filter(code = Code(word))
    return RenderWithInf('helper/results.html', request, {
        'words': existing_words, 'whose': 'all'})

def Delete(request, where, word):
    if request.user.username:
        word_to_delete = Word.objects.get(word = word, added_by = request.user)
        if word_to_delete.added_by.count() > 1:
            word_to_delete.added_by.remove(request.user)
        else:
            word_to_delete.delete()
    else:
        messages.error(request, 'nie możesz usunąć słowa, \
                które nie należy do Ciebie')
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


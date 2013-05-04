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
from helper.forms import AddForm, FindForm

def AddPage(request):
    if request.POST:
        form = AddForm(request.POST, request.FILES)
        if not request.user.username:
            messages.error(request, 'by dodać jakiekolwiek słowo \
                    musisz być zalogowany')
        elif form.is_valid(): 
            words = form.cleaned_data['words']
            wordsfile = form.cleaned_data['wordsfile']
            language = form.cleaned_data['language']
            if words:
                AddWords(words, language, request)
            if wordsfile:
                file = request.FILES['wordsfile']
                if file:
                    AddWords(file.read().decode('utf-8'), language, request)
                else:
                    messages.error(request, 'nie wybrano pliku do dodania')
    else:
        form = AddForm()
    return RenderWithInf('helper/add.html', request, {'form': form})

def FindPage(request, word=''):
    existing_words = []
    if request.POST:
        form = FindForm(request.POST)
        if form.is_valid():
            where = form.cleaned_data['where']
            word = form.cleaned_data['letters']
            language = form.cleaned_data['language']
            if '*' in word:
                for letter in u'abcdefghijklmnoprstuwyzęóąśłżźćń':
                    existing_words.extend(Word.objects.filter(
                        code = Code(word.replace('*', letter)), 
                        added_by__in = where, language = language))
            else:
                existing_words = Word.objects.filter(code = Code(word), 
                    added_by__in = where, language = language) 
    else:
        form = FindForm()
    return RenderWithInf('helper/find.html', request, {
        'form':form, 'word': word, 'words': existing_words, 'whose': 'all'})
            
def AddWord(request, word, where):
    if request.user.username:
        if AddOne(word, language, request.user):
            messages.info(request, u'Dodano wyraz <{}>'.format(word))
    else:
        messages.error(request, 'by dodać jakiekolwiek słowo musisz być zalogowany')
    return HttpResponseRedirect(where)

def AddWords(text, language, request):
    how_many = 0
    for word in re.split('[\s,?!;:()-]', text):
        if re.search('[."\']', word) == None:
            how_many += AddOne(word, language, request.user)
    if how_many == 1:
        messages.info(request, 'dodano słowo')
    elif 1 < how_many < 5:
        messages.info(request, 'dodano ' + str(how_many) + ' słowa')
    else:
        messages.info(request, 'dodano ' + str(how_many) + ' słów')

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
    return HttpResponseRedirect(reverse('find'))

def AddOne(word, language, added_by):
    if word == word.lower() and 1 < len(word) < 9:
        word, created = Word.objects.get_or_create(code = Code(word),
                word = word, language = language,  points = SetPoints(word))
        if not Word.objects.filter(word = word, added_by = added_by).exists(): 
            word.added_by.add(added_by)
            return 1
    return 0

def Code(word):
    return ''.join(sorted(word[:]))

def SetPoints(word):
    return len(word)


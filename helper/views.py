#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import itertools, urllib, re
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from scrabble.models import Word, User, Language
from scrabble.views import RenderWithInf
from helper.forms import AddForm, FindForm

def AddPage(request):
    added_words = []
    if request.POST:
        form = AddForm(request.POST, request.FILES)
        if not request.user.username:
            messages.error(request, 'by dodać jakiekolwiek słowo \
                    musisz być zalogowany')
        elif form.is_valid(): 
            words = form.cleaned_data['words']
            wordsfile = form.cleaned_data['wordsfile']
            if words:
                added_words.extend(AddWords(request, words))
            if wordsfile:
                file = request.FILES['wordsfile']
                if file:
                    added_words.extend(AddWords(request, 
                        file.read().decode('utf-8')))
                else:
                    messages.error(request, 'nie wybrano pliku do dodania')
    else:
        form = AddForm()
    return RenderWithInf('helper/add.html', request, {'form': form, 
        'added_words': added_words})

def FindPage(request, word=''):
    existing_words = []
    if request.POST:
        form = FindForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['letters']
            language = request.session.get('language', 'pl')
            language = Language.objects.get(short = language)
            if form.cleaned_data['how'] == '3':
                where = form.cleaned_data['where']
                if '*' in word:
                    for letter in language.letters:
                        existing_words.extend(Word.objects.filter(
                            code = Code(word.replace('*', letter)), 
                            added_by__in = where, language = language))
                else:
                    existing_words = Word.objects.filter(code = Code(word), 
                        added_by__in = where, language = language) 
            elif form.cleaned_data['how'] == '2':
                if '*' in word:
                    for letter in language.letters:
                        existing_words.extend(Word.objects.filter(
                            code = Code(word.replace('*', letter)), 
                            language = language))
                else:
                    existing_words = Word.objects.filter(code = Code(word), 
                    language = language) 
            elif form.cleaned_data['how'] == '1':
                if not request.user.username:
                    messages.error(request, 'Aby skorzystać z tej opcji \
                            musisz być zalogowany')
                else:
                    where = User.objects.get(username = request.user)
                    if '*' in word:
                        for letter in language.letters:
                            existing_words.extend(Word.objects.filter(
                                code = Code(word.replace('*', letter)), 
                                added_by = where, language = language))
                    else:
                        existing_words = Word.objects.filter(code = Code(word), 
                            added_by = where, language = language) 
    else:
        form = FindForm()
    return RenderWithInf('helper/find.html', request, {
        'form':form, 'word': word, 'words': existing_words, 'whose': 'all'})
            
def AddWord(request, word, where):
    if request.user.username:
        language = request.session.get('language', 'pl')
        language = Language.objects.get(short = language) 
        if AddOne(word, language, request.user):
            messages.info(request, u'Dodano wyraz <{}>'.format(word))
    else:
        messages.error(request, 'by dodać jakiekolwiek słowo musisz być zalogowany')
    return HttpResponseRedirect(where)

def AddWords(request, text):
    added_words = []
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short = language)
    for word in re.split('[\s,?!;:()-]', text):
        if re.search('[."\']', word) == None:
            if AddOne(word, language, request.user):
                added_words.append(word)
    how_many = len(added_words)
    if how_many == 1:
        messages.info(request, 'dodano słowo')
    elif 1 < how_many % 10 < 5:
        messages.info(request, 'dodano ' + str(how_many) + ' słowa')
    else:
        messages.info(request, 'dodano ' + str(how_many) + ' słów')
    return added_words

def Delete(request, words, word):
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short = language)
    word_to_delete = Word.objects.filter(word = word, added_by = request.user,
            language = language)
    if word_to_delete:
        word_to_delete = word_to_delete[0] 
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

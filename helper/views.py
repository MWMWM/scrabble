#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import re
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import messages
from scrabble.models import Word, User, Language
from scrabble.views import RenderWithInf
from helper.forms import AddForm, FindForm

def AddPage(request):
    if request.POST:
        form = AddForm(request.POST, request.FILES)
        if not request.user.username:
            messages.error(request, 'By dodać jakiekolwiek słowo \
                    musisz być zalogowany')
        elif form.is_valid():
            words = form.cleaned_data['words']
            wordsfile = form.cleaned_data['wordsfile']
            if words:
                AddWords(request, words)
            if wordsfile:
                file = request.FILES['wordsfile']
                if file:
                    AddWords(request, file.read().decode('utf-8'))
                else:
                    messages.error(request, 'Nie wybrano pliku do dodania')
    else:
        form = AddForm()
    return RenderWithInf('helper/add.html', request, {'form': form})

def FindPage(request, word=''):
    if request.POST:
        form = FindForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['letters']
            language = request.session.get('language', 'pl')
            language = Language.objects.get(short=language)
            if form.cleaned_data['how'] == '3':  # z danych wybranych osób
                where = form.cleaned_data['where']
            elif form.cleaned_data['how'] == '2':  # ze wszystkich użytkowników
                where = User.objects.all()
            elif form.cleaned_data['how'] == '1':  # z danych użytkownika
                if not request.user.username:
                    messages.error(request, 'Aby skorzystać z tej opcji \
                            musisz być zalogowany')
                else:
                    user = User.objects.get(username=request.user)
                    where = [user, ]
            if '*' in word:
                for_regex = ['^' + r'?'.join(Code(word.replace('*', letter))) \
                        + '?$' for letter in language.letters]
                my_regex = '(' + '|'.join(for_regex) + ')'
            else:
                my_regex = r'^' + r'?'.join(Code(word)) + '?$'
            existing_words = Word.objects.filter(code__regex=my_regex,
                    language=language, added_by__in=where).order_by('-points')
    else:
        existing_words = []
        form = FindForm()
    return RenderWithInf('helper/find.html', request, {
        'form': form, 'word': word, 'words': existing_words})

def AddWord(request, word, where):
    if request.user.username:
        language = request.session.get('language', 'pl')
        language = Language.objects.get(short=language)
        if AddOne(word, language, request.user):
            messages.info(request, u'Dodano wyraz <{}>'.format(word))
    else:
        messages.error(request, 'By dodać jakieś słowo musisz być zalogowany')
    return HttpResponseRedirect(where)

def AddWords(request, text):
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    t = threading.Thread(target=AddWordsT, kwargs={'language': language,
        'text': text, 'user': request.user})
    t.setDaemon(True)
    t.start()
    return True

def AddWordsT(language, text, user):
    for word in re.split('[\s,?!;:()-]', text):
        if re.search('[."\']', word) == None:
            AddOne(word, language, user)

def Delete(request, word, where):
    language = request.session.get('language', 'pl')
    language = Language.objects.get(short=language)
    word_to_delete = Word.objects.filter(word=word, added_by=request.user,
            language=language)
    if word_to_delete:
        word_to_delete = word_to_delete[0]
        if word_to_delete.added_by.count() > 1:
            word_to_delete.added_by.remove(request.user)
        else:
            word_to_delete.delete()
    else:
        messages.error(request, 'Nie możesz usunąć słowa, \
                które nie należy do Ciebie')
    return HttpResponseRedirect(where)

def CheckSubwords(word, language):
    for_regex = '^' + r'?'.join(Code(word)) + '?$'
    words = Word.objects.filter(code__regex=for_regex, language=language)
    return words

def AddOne(word, language, added_by):
    if word == word.lower() and 1 < len(word) < 9:
        word, created = Word.objects.get_or_create(code=Code(word),
                word=word, language=language,  points=SetPoints(word))
        if not Word.objects.filter(word=word, added_by=added_by).exists():
            word.added_by.add(added_by)
            return 1
    return 0

def Code(word):
    return ''.join(sorted(word[:]))

def SetPoints(word):
    return len(word)

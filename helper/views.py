#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import re
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from scrabble.models import Word, User, Language, SetPoints
from helper.forms import AddForm, FindForm
import magic
import subprocess


def AddPage(request):
    if request.POST:
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            words = form.cleaned_data['words']
            wordsfile = form.cleaned_data['wordsfile']
            if words:
                AddWords(request, words)
            if wordsfile:
                file = request.FILES['wordsfile']
                if file:
                    AddWords(request, file.read())
                else:
                    messages.error(request, 'Nie wybrano pliku do dodania')
    else:
        form = AddForm()
    return render_to_response('helper/add.html', {'form': form},
            context_instance=RequestContext(request))

def FindPage(request, word=''):
    existing_words = []
    if request.POST:
        form = FindForm(request.user, request.POST)
        if form.is_valid():
            word = form.cleaned_data['letters']
            adders = form.cleaned_data['adders']
            language = request.session.get('language', 'pl')
            language = Language.objects.get(short=language)
            if '*' in word:
                for_regex = ['^' + r'?'.join(Code(word.replace('*', letter))) \
                        + '?$' for letter in language.letters]
                my_regex = '(' + '|'.join(for_regex) + ')'
            else:
                my_regex = r'^' + r'?'.join(Code(word)) + '?$'
            existing_words = Word.objects.filter(code__regex=my_regex,
                    language=language, added_by__in=adders).order_by('-points')
    else:
        form = FindForm(request.user)
    return render_to_response('helper/find.html', {'form': form, 'word': word, 
        'words': existing_words}, context_instance=RequestContext(request))

def AddWord(request, word, where):
    if request.user.username:
        language = request.session.get('language', 'pl')
        language = Language.objects.get(short=language)
        if AddOne(word, language, request.user):
            messages.info(request, u'Dodano wyraz <{}>'.format(word))
    else:
        messages.error(request, 'By dodać jakieś słowo musisz być zalogowany')
    return HttpResponseRedirect(where)

def GetRawText(file, request):
    file_type = magic.from_buffer(file, mime=True)
    if file_type == 'text/plain':
        file_type = magic.from_buffer(file)
        if file_type == 'ASCII text':
            return file
        if file_type ==  'UTF-8 Unicode text':
            return file.decode('utf-8')
        elif 'UTF-16' in file_type:
            return file.decode('utf-16')
        else:
            messages.error(request, 'Nie rozpoznaję kodowania pliku')
    elif file_type == 'application/pdf':
        messages.error(request, 'Ten format nie jest jeszcze obsługiwany')
    else:
        messages.error(request, 'Ten format nie jest obsługiwany')
    return None


def AddWords(request, text):
    text = GetRawText(text, request)
    if text:
        language = request.session.get('language', 'pl')
        language = Language.objects.get(short=language)
        messages.info(request, u'Twoje słowa są dodawane do bazy')
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
    try:
        word_to_delete = Word.objects.get(word=word, added_by=request.user,
            language=language)
        word_to_delete.delete()
    except (IndexError, ObjectDoesNotExist, DatabaseError):
        messages.error(request, 'Nie możesz usunąć tego słowa')
    return HttpResponseRedirect(where)

def CheckSubwords(letters, language):
    for_regex = '^' + r'?'.join(Code(letters)) + '?$'
    words = Word.objects.filter(code__regex=for_regex, language=language)
    return words

def AddOne(word, language, added_by):
    if word == word.lower() and 1 < len(word) < 9:
        word, created = Word.objects.get_or_create(code=Code(word),
                word=word, language=language, points=SetPoints(word))
        if not Word.objects.filter(word=word, added_by=added_by).exists():
            word.added_by.add(added_by)
            return 1
    return 0

def Code(word):
    return ''.join(sorted(word[:]))

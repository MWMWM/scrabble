#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import re
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from scrabble.models import Word, User, Language, SetPoints
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
    return render_to_response('helper/add.html', {'form': form},
            context_instance=RequestContext(request))

def FindPage(request, word=''):
    if request.POST:
        form = FindForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['letters']
            if form.cleaned_data['how'] == '3':  # z danych wybranych osób
                adders = form.cleaned_data['where']
            elif form.cleaned_data['how'] == '2':  # ze wszystkich użytkowników
                adders = User.objects.all()
            elif form.cleaned_data['how'] == '1':  # z danych użytkownika
                if not request.user.username:
                    messages.error(request, 'Aby skorzystać z tej opcji \
                            musisz być zalogowany')
                    adders =[]
                else:
                    user = User.objects.get(username=request.user)
                    adders = [user, ]
            language = request.session.get('language', 'pl')
            language = Language.objects.get(short=language)
            existing_words = []
            if '*' in word:
                for letter in language.letters:
                    for adder in adders:
                        existing_words += Word.objects.filter(
                                code=Code(word.replace('*', letter)), 
                                language=language, added_by=adder).order_by('-points')
            else:
                for adder in adders:
                    existing_words += Word.objects.filter(code=Code(word),
                        language=language, added_by=adder).order_by('-points')
    else:
        existing_words = []
        form = FindForm()
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
    try:
        word_to_delete = Word.objects.get(word=word, added_by=request.user,
            language=language)
        word_to_delete.delete()
    except IndexError:
        messages.error(request, 'Nie możesz usunąć słowa, \
                które nie należy do Ciebie')
    return HttpResponseRedirect(where)

def CheckSubwords(word, language):
    words = Word.objects.filter(code=Code(word), language=language)
    return words

def AddOne(word, language, added_by):
    if word == word.lower() and 1 < len(word) < 9:
        if not Word.objects.filter(word=word, language=language, added_by=added_by).exists():
            Word.objects.create(code=Code(word), word=word, language=language,  
                    points=SetPoints(word), added_by=added_by)
            return 1
    return 0

def Code(word):
    return ''.join(sorted(word[:]))

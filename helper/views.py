#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools, urllib
from helper.models import Word
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import re

def ShowForm(request):
    if request.method == 'POST':
        if 'find' in request.POST:
            where = request.POST.get('where', '')
            word = request.POST.get('word_to_check', '')
        if 'add' in request.POST:
            where = request.POST.get('howmany', '')
            if where == 'AddMultiple' and 'plik' in request.FILES:
                AddMultiple(request.FILES['plik'])
                return HttpResponseRedirect('/help')
            word = request.POST.get('word_to_add', '')
        direction = '/help/' + where + '/' + word
        return HttpResponseRedirect(direction)
    return render_to_response('helper/form.html', {}, RequestContext(request))

def SjpResult(request, word):
    """
    szuka w oparciu o stronę sjp.pl,
    bardzo wolne
    """
    existing_words = []
    letters = [ letter for letter in word ]
    for temp_letters in itertools.permutations(letters):
        temp_word = ''.join((temp_letter for temp_letter in temp_letters))
        if Check(temp_word):
            existing_words.append(temp_word)
    return render_to_response('helper/results.html', {'words': existing_words}, RequestContext(request))

def DbResult(request, word):
    """
    sprawdza, czy można utworzyć słowo, znajdujące się w bazie, 
    wykorzystując wszystkie podane literki
    """
    code = Code(word)
    existing_words = Word.objects.filter(code=code)
    return render_to_response('helper/results.html', {'words': existing_words}, RequestContext(request))

def AddOne(request, word):
    AddWord(word)
    return HttpResponseRedirect('/help')

def AddMultiple(file):
    """
    dodaje wszystkie słowa z podanego pliku do bazy
    pomija wszystkie słowa z cudzysłowem, kropką lub zawierające wielkie litery
    (mniejsze prawdopodobieństwo dodania nazw własnych i skrótów)
    """
    text = file.read()
    for word in re.split('[\s,?!;:()-]', text):
        if re.search('[."\']', word) == None:
            AddWord(word.decode('utf-8'))

def Check(word):
    path = u'http://www.sjp.pl/{0}'.format(word).encode('utf-8')
    for line in urllib.urlopen(path):
        if 'słowo nie występuje w słowniku' in line or 'niedopuszczalne w grach' in line:
            return 0
        if 'dopuszczalne w grach' in line:
            return 1

def AddWord(word):
    if word == word.lower():
        code = Code(word)
        if not Word.objects.filter(code=code):
            word_to_add = Word(word=word, code=code)
            print word_to_add
            word_to_add.save()

def Code(word):
    return ''.join(sorted(word[:]))

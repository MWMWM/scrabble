#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools, urllib, re
from helper.models import Word, User
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def ShowForm(request):
    info = []
    if 'logout' in request.POST:           
        logout(request)
    if 'login' in request.POST or 'addlogin' in request.POST:
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        if 'addlogin' in request.POST and not User.objects.filter(username = name):
                p = User.objects.create_user(username = name, password = password)
        person = authenticate(username = name, password = password)
        if person is not None:
            login(request, person)
        else:
            info.append(u'błąd logowania')
    if 'find' in request.POST:
        where = request.POST.get('where', '')
        word = request.POST.get('word_to_check', '')
        direction = '/help/' + where + '/' + word
        return HttpResponseRedirect(direction)
    user = request.user
    if user.username == 'AnonymousUser':
        user.username=""
    if 'add' in request.POST and user.username:
        where = request.POST.get('howmany', '')
        if where == 'AddMultiple':
            if 'plik' in request.FILES:
                AddMultiple(request.FILES['plik'], user)
                info.append(u'Twój plik został dodany')
            else:
                info.append(u'Błąd: brak pliku')
        elif where == 'AddOne':
            word = request.POST.get('word_to_add', '')
            if AddOne(word, user):
                    info.append(u'dodano wyraz <{}>'.format(word))
            else:
                info.append(u'słowo <{}> jest już w Twojej bazie'.format(word))
    return render_to_response('helper/form.html', {'user': user.username, 'info': info}, RequestContext(request))

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

def MyResult(request, word):
    code = Code(word)
    existing_words = Word.objects.filter(code=code, added_by=request.user)
    return render_to_response('helper/results.html', {'words': existing_words}, RequestContext(request))

def Delete(request, word):
    person = request.user
    word_to_delete = Word.objects.filter(word = word, added_by = person)
    if word_to_delete:
        to_delete = word_to_delete[0]
        if to_delete.added_by.count() > 1:
            to_delete.added_by.remove(person)
        else:
            to_delete.delete()
    return HttpResponseRedirect('/help/DbResult/'+word)

def AddMultiple(file, added_by):
    """
    dodaje wszystkie słowa z podanego pliku do bazy
    pomija wszystkie słowa z cudzysłowem, kropką lub zawierające wielkie litery
    (mniejsze prawdopodobieństwo dodania nazw własnych i skrótów)
    """
    text = file.read()
    for word in re.split('[\s,?!;:()-]', text):
        if re.search('[."\']', word) == None:
            AddOne(word.decode('utf-8'), added_by)

def AddOne(word, added_by):
    if word == word.lower():
        if not Word.objects.filter(word = word):
           code = Code(word) 
           word_to_add = Word(word = word, code = code)
           word_to_add.save()
        if not Word.objects.filter(word=word, added_by = added_by):
            word_to_add = Word.objects.get(word=word)
            word_to_add.added_by.add(added_by)
            return 1

def Code(word):
    return ''.join(sorted(word[:]))

def Check(word):
    path = u'http://www.sjp.pl/{0}'.format(word).encode('utf-8')
    for line in urllib.urlopen(path):
        if 'słowo nie występuje w słowniku' in line or 'niedopuszczalne w grach' in line:
            return 0
        if 'dopuszczalne w grach' in line:
            return 1

#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools, urllib, re
from helper.models import Word, User
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

def RenderWithInf(template, request, args={}):
    words_number = Word.objects.distinct().count()
    messages.info(request, 'w bazie jest obecnie ' + str(words_number) + ' słów')
    user = request.user
    if not user.username:
        messages.info(request, 'nie jesteś zalogowany')
    else:
        messages.info(request, u'jesteś zalogowany jako: ' + user.username)
    return render_to_response (template, args, context_instance=RequestContext(request))

def Login(request):
    if request.POST:
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        if 'addlog' in request.POST:
            if not User.objects.filter(username = name):
                User.objects.create_user(username = name, password = password)
        person = authenticate(username = name, password = password)
        if person is not None:
            login(request, person)
            try:
                where = request.get_full_path().split('?next=')[1]
            except IndexError:
                where = '/help/'
            return HttpResponseRedirect(where)
        else:
            messages.error(request, 'Błąd: podano nieprawidłowe dane')
            if User.objects.filter(username = name):
                messages.error(request, 'taki login istnieje, ale hasło nie odpowiada temu kontu')
            else:
                messages.error(request, 'taki login nie istnieje')
    return RenderWithInf('helper/login.html', request)

def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))

def Main(request):
    if 'find' in request.POST:
        storage = messages.get_messages(request)
        storage.used = True
        where = request.POST.get('where', '')
        word = request.POST.get('word_to_check', '')
        direction = '/help/' + where + '/' + word
        return HttpResponseRedirect(direction)
    if 'add' in request.POST:
        where = request.POST.get('howmany', '')
        if where == 'AddMultiple':
            return AddWords(request)
        elif where == 'AddOne':
            word = request.POST.get('word_to_add', '')
            return HttpResponseRedirect('/help/AddWord/' + word)
    return RenderWithInf('helper/form.html', request)

@login_required(login_url='/login/')
def AddWord(request, word):
    user = request.user
    if AddOne(word, user):
        messages.info(request, u'Dodano wyraz <{}>'.format(word))
    else:
        messages.info(request, u'Słowo <{}> jest już w Twojej bazie'.format(word))
    return HttpResponseRedirect(reverse('main'))

@login_required(login_url='/login/')
def AddWords(request):
    file = request.FILES['plik']
    if file:
        text = file.read()
        how_many = 0
        for word in re.split('[\s,?!;:()-]', text):
            if re.search('[."\']', word) == None:
                how_many += AddOne(word.decode('utf-8'), request.user)
        messages.info(request, 'dodano ' + str(how_many) + ' słów')
    else:
        messages.error(request, 'nie wybrano pliku do dodania')
    return HttpResponseRedirect(reverse('main'))

def DbResult(request, word):
    letters = [letter for letter in u'wertyuioplkjhgfdsazcbnmęóąśłżźćń']
    if '.' in word:
        existing_words = []
        for letter in letters:
            existing_words.extend(Word.objects.filter(code = Code(word.replace('.', letter))))
    else:
        existing_words = Word.objects.filter(code = Code(word))
    return RenderWithInf('helper/results.html', request, {'words': existing_words})

def MyResult(request, word):
    letters = [letter for letter in u'wertyuioplkjhgfdsazcbnmęóąśłżźćń']
    if '.' in word:
        existing_words = []
        for letter in letters:
            existing_words.extend(Word.objects.filter(
                code = Code(word.replace('.', letter)), 
                added_by = request.user))
    else:
        existing_words = Word.objects.filter(code = Code(word), added_by = request.user)
    return RenderWithInf('helper/results.html', request, {'words': existing_words})

@login_required(login_url='/login/')
def Delete(request, word, prev):
    if Word.objects.filter(word = word, added_by = request.user).exists():
        word_to_delete = Word.objects.get(word = word)
        if word_to_delete.added_by.count() > 1:
            word_to_delete.added_by.remove(request.user)
        else:
            word_to_delete.delete()
    return HttpResponseRedirect('/help/DbResult/' + prev)

def AddOne(word, added_by):
    if word == word.lower() and len(word) < 9:
        word, created = Word.objects.get_or_create(word = word, code = Code(word))
        if not Word.objects.filter(word = word, added_by = added_by).exists():
            word_to_add = Word.objects.get(word = word)
            word_to_add.added_by.add(added_by)
            return 1
    return 0

def Code(word):
    return ''.join(sorted(word[:]))


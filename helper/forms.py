#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from scrabble.models import Word, User

class AddForm(forms.Form):
    words = forms.CharField(max_length=200, required=False,
            label="słowo/a (podaj oddzielane przecinkami)")
    wordsfile = forms.FileField(required=False,
            label="plik tekstowy ze słowami, które chcesz dodać") 
    language = forms.CharField(max_length=2, label="język", 
            widget=forms.Select(choices=Word.lang_choices))

class FindForm(forms.Form):
    letters = forms.CharField(max_length=10, label=" z literek")
    where = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
            label="wykorzystując dane użytkownika/użytkowników")

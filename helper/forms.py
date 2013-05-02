#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from helper.views import Word

class AddForm(forms.Form):
    words = forms.CharField(max_length=200, required=False,
            label="słowo/a (podaj oddzielane przecinkami)")
    wordsfile = forms.FileField(required=False,
            label="plik tekstowy ze słowami, które chcesz dodać") 
    language = forms.CharField(max_length=2, label="język", 
            widget=forms.Select(choices=Word.lang_choices))


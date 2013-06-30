#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from scrabble.models import Word, User

class AddForm(forms.Form):
    words = forms.CharField(max_length=200, required=False,
            label="słowo/a (podaj oddzielane przecinkami)")
    wordsfile = forms.FileField(required=False,
            label="słowa z pliku (w formacie .txt)")

class FindForm(forms.Form):
    lookup_options = ((1, 'moich',), (2, 'wszystkich',),
            (3, 'pozwól mi wybrać osoby',))
    letters = forms.CharField(max_length=10, label=" z literek (możesz użyć blanka - zastąp go znakiem *)")
    how = forms.ChoiceField(choices=lookup_options, 
            label="z danych")
    where = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            label="wykorzystując dane użytkownika/użytkowników",
            widget=forms.SelectMultiple,
            #widget=forms.CheckboxSelectMultiple,
            required=False)

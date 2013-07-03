#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from django import forms
from scrabble.models import Word, User


class AddForm(forms.Form):
    words = forms.CharField(max_length=200, required=False,
            label="słowo/a (podaj oddzielane przecinkami)")
    wordsfile = forms.FileField(required=False,
            label="słowa z pliku (w formacie .txt)")

    def clean_words(self):
        words = self.cleaned_data['words']
        if re.search('[."\'-<>\d?!;:()/]', words):
            return ValidationError("Wpisano niedozwolone znaki")
        return words


class FindForm(forms.Form):
    letters = forms.CharField(max_length=10, 
            label=" z literek (możesz użyć blanka - zastąp go znakiem *)")
    adders = forms.ChoiceField(choices=(), label="z danych")

    def __init__(self, user=None, *args, **kwargs):
        super(FindForm, self).__init__(*args, **kwargs)
        self.user = user
        lookup_options = (('wszystkich', 'wszystkich'), )
        if self.user.username:
            lookup_options +=(('moich', 'moich'), )
        more_lookup_options = [(person, person) for person in User.objects.all()]
        all_lookup_options = lookup_options + tuple(more_lookup_options)
        self.fields['adders'].choices = all_lookup_options

    def clean_adders(self):
        adders = self.cleaned_data['adders']
        if adders == 'wszystkich':
            return User.objects.all()
        elif adders == 'moich':
            if not self.user.username:
                raise forms.ValidationError('Nie jesteś zalogowany')   
            else:
                 return [User.objects.get(username=self.user), ]
        else:
            return [User.objects.get(username=adders), ]
    

#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from django import forms
from scrabble.models import Word, User, Language


class AddForm(forms.Form):
    words = forms.CharField(max_length=200, required=False,
            widget=forms.Textarea(attrs={'rows':5}),
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

class LangForm(forms.ModelForm):
    instances = forms.CharField(max_length=1000,
            widget=forms.Textarea(attrs={'rows':5}),
            label="przykłady słów w tym języku (oddziel je tylko spacjami)")
    short = forms.CharField(max_length=2, label='dwuliterowy skrót')
    name = forms.CharField(max_length=20, label='pełna nazwa')
    letters = forms.CharField(max_length=50,label='alfabet')

    class Meta:
        model = Language
 
    def clean_letters(self):
        letters = self.cleaned_data['letters']
        if len(letters) < 10:
            raise forms.ValidationError('Zbyt mało literek ma ten alfabet')
        if len(letters) != len(set(letters)):
            raise forms.ValidationError('Literki się powtarzają')
        return letters

    def clean_short(self):
        short_name = self.cleaned_data['short']
        if len(short_name) != 2:
            raise forms.ValidationError('skrót ma mieć dwie literki')
        return short_name

    def clean(self):
        cleaned_data = super(LangForm, self).clean()
        letters = cleaned_data.get('letters')
        instances = cleaned_data.get('instances')
        if letters and instances:
            for word in instances.split():
                if not set(word).issubset(set(letters)):
                    raise forms.ValidationError(u"Słowo {} zawiera literę/y, których nie ma w alfabecie".format(word))
        return cleaned_data

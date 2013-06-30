# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import random

class Language(models.Model):
    short = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=20)
    letters = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Word(models.Model):
    code = models.CharField(max_length=20, db_index=True)
    word = models.CharField(max_length=20)
    added_by = models.ForeignKey(User)
    language = models.ForeignKey(Language)
    points = models.IntegerField()
    class Meta:
        ordering = ('points', 'word')
    def __unicode__(self):
        return self.word

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True)
    best_score = models.IntegerField(default=0)
    last_score = models.IntegerField(default=0)
    last_temp_letters = models.CharField(max_length=12)
    last_all_letters = models.CharField(max_length=12)
    def __unicode__(self):
        return self.user.username
    def prepare_for_play(self, language):
        self.last_all_letters = "".join(NewLetters(language, 8))
        self.last_temp_letters = ""
        if self.best_score < self.last_score:
            self.best_score = self.last_score
        self.last_score = 0
        self.save()

def NewLetters(language, how_many=1):
        return random.sample(language.letters, how_many)

points_table = {'a':1, u'ą':5, 'b':3, 'c':2, u'ć':6, 'd':2, 'e':1, u'ę':5, 'f':5,
'g':3, 'h':3, 'i':1, 'j':3, 'k':2, 'l':2, u'ł':3, 'm':2, 'n':1, u'ń':7, 'o':1,
u'ó':5, 'p':2, 'q':2, 'r':1, 's':1, u'ś':5, 't':2, 'u':3, 'v':2, 'w':1, 'x':3,
'y':2, 'z':1, u'ź':9, u'ż':5}

def SetPoints(word):
    points = 0
    for i in word:
        points += points_table[i]
    return points

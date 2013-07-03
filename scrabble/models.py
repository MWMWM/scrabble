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

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True)
    best_score = models.IntegerField(default=0)
    last_score = models.IntegerField(default=0)
    last_temp_letters = models.CharField(max_length=12, default='')
    last_all_letters = models.CharField(max_length=12, default='')
    def __unicode__(self):
        return self.user.username
    def prepare_for_play(self, language):
        self.last_all_letters = "".join(NewLetters(language, 8))
        self.last_temp_letters = ""
        if self.best_score < self.last_score:
            self.best_score = self.last_score
        self.last_score = 0
        self.save()

class Word(models.Model):
    code = models.CharField(max_length=20, db_index=True)
    word = models.CharField(max_length=20)
    added_by = models.ManyToManyField(User)
    language = models.ForeignKey(Language)
    points = models.IntegerField()
    class Meta:
        ordering = ('points', 'word')
    def __unicode__(self):
        return self.word

def NewLetters(language, how_many=1):
        return random.sample(language.letters, how_many)

points_table = {u'a':1, u'ą':5, u'b':3, u'c':2, u'ć':6, u'd':2, u'e':1, u'ę':5,
u'f':5, u'g':3, u'h':3, u'i':1, u'j':3, u'k':2, u'l':2, u'ł':3, u'm':2, u'n':1,
u'ń':7, u'o':1, u'ó':5, u'p':2, u'q':2, u'r':1, u's':1, u'ś':5, u't':2, u'u':3,
u'v':2, u'w':1, u'x':3, u'y':2, u'z':1, u'ź':9, u'ż':5}

def SetPoints(word):
    points = 0
    for i in word:
        points += points_table[i]
    return points

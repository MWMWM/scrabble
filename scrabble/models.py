from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
    code = models.CharField(max_length = 9, db_index=True) 
    word = models.CharField(max_length = 9, primary_key=True)
    added_by = models.ManyToManyField(User)
    lang_choices = (('pl', 'polski'), ('en', 'english'),)
    language = models.CharField(max_length=2, choices=lang_choices, default='pl')
    def __unicode__(self):
        return self.word
    def str(self):
        return self.word


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    best_score = models.IntegerField(default=0)
    language = models.CharField(max_length=2, choices=Word.lang_choices, default='pl')
    def __unicode__(self):
        return self.user.username 

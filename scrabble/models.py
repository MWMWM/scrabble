from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    short = models.CharField(max_length = 2, unique=True)
    name = models.CharField(max_length = 20)
    letters = models.CharField(max_length = 100)
    def __unicode__(self):
        return self.name

class Word(models.Model):
    code = models.CharField(max_length = 9, db_index=True) 
    word = models.CharField(max_length = 9)
    added_by = models.ManyToManyField(User)
    language = models.ForeignKey(Language) 
    points = models.IntegerField()
    class Meta:
        ordering = ('points', 'word')
    def __unicode__(self):
        return self.word

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True)
    best_score = models.IntegerField(default=0)
    def __unicode__(self):
        return self.user.username

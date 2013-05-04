from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
    code = models.CharField(max_length = 9, db_index=True) 
    word = models.CharField(max_length = 9)
    added_by = models.ManyToManyField(User)
    lang_choices = (('pl', 'polski'), ('en', 'english'),)
    language = models.CharField(max_length=2, choices=lang_choices, 
            default='pl')
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

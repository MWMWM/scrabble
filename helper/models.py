from django.db import models

class Word(models.Model):
    code = models.CharField(max_length=9)
    word = models.CharField(max_length=9, unique=True, primary_key=True)
    def __unicode__(self):
        return self.word


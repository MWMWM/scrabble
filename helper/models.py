from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
	code = models.CharField(max_length = 9)
	word = models.CharField(max_length = 9)
	added_by = models.ManyToManyField(User)	
	def __unicode__(self):
		return self.word

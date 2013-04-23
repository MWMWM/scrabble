from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    temp_score = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)
    lang_choices = (('pl', 'polski'), ('en', 'english'),)
    lang = models.CharField(max_length=2, choices=lang_choices, default='pl')
    def __unicode__(self):
        return self.user.username 

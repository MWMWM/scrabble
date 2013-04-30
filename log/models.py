from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    best_score = models.IntegerField(default=0)
    lang_choices = (('pl', 'polski'), ('en', 'english'),)
    language = models.CharField(max_length=2, choices=lang_choices, default='pl')
    def __unicode__(self):
        return self.user.username 

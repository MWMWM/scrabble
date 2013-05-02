from django.contrib import admin
from scrabble import models

admin.site.register(models.Word)
admin.site.register(models.UserProfile)


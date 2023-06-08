from django.contrib import admin

# Register your models here.
from directory import models

admin.site.register(models.UserProfile)
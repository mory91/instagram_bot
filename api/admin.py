from django.contrib import admin
from .models import Target
from .models import Bot

# Register your models here.

admin.site.register(Target)
admin.site.register(Bot)

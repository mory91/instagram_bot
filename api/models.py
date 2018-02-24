from django.db import models

# Create your models here.
class Target(models.Model):
    TYPES = (
        ('T', 'Tag'),
        ('P', 'Page'),
        ('L', 'Place'),
    )
    target = models.CharField(max_length=30)
    target_type = models.CharField(max_length=1, choices=TYPES)
    target_action = models.CharField(max_length=3)

class Reset(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

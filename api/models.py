from django.db import models

# Create your models here.
class Target(models.Model):
    TYPES = (
        ('T', 'Tag'),
        ('P', 'Page'),
        ('L', 'Place'),
    )
    FOLLOWS = (
        ('F', 'Followers'),
        ('L', 'Likers'),
    )
    target = models.CharField(max_length=30)
    target_type = models.CharField(max_length=1, choices=TYPES)
    target_action = models.CharField(max_length=3)
    target_follows = models.CharField(max_length=1, choices=FOLLOWS)
    blocked = models.BooleanField(default = False)
    bot = models.ForeignKey(
        'Bot',
        on_delete=models.CASCADE,
    )

class Reset(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    bot = models.ForeignKey(
        'Bot',
        on_delete=models.CASCADE,
    )

class Bot(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    like_per_day = models.IntegerField(default=500)
    comment_per_day = models.IntegerField(default=50)
    unfollow_per_day = models.IntegerField(default=100)
    follow_per_day = models.IntegerField(default=100)
    comments = models.TextField()
    second_username = models.CharField(max_length=30, null=True, blank=True)
    second_password = models.CharField(max_length=30, null=True, blank=True)
    state = models.IntegerField(default=-1)
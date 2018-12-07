from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    bio = models.CharField(max_length=500)
    display_name = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    website = models.URLField()
    # profile_photo = models.ImageField()
    # header_photo = models.ImageField()


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=1000)
    time_tweeted = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    time_liked = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    time_reply = models.DateTimeField(auto_now_add=True)
    reply_text = models.CharField(max_length=1000)


class Follow(models.Model):
    user_follow = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')
    user_followed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed')
    time_start_follow = models.DateTimeField(auto_now_add=True)

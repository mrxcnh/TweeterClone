from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.
from tweeter.models import Tweet


class IndexView(generic.ListView):
    template_name = 'tweeter/index.html'
    context_object_name = 'tweet_list'

    def get_queryset(self):
        return Tweet.objects.all()


def add_tweet(request):
    current_user = request.user
    user_id = current_user.id
    current_time = timezone.now()
    new_tweet = Tweet.objects.create(user_id=user_id, tweet_text=request.POST['tweet_text'], time_tweeted=current_time)
    new_tweet.save()
    return HttpResponseRedirect(reverse('tweeter:index'))

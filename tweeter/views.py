from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
from django.utils import timezone

# Create your views here.
from tweeter.models import Tweet, Like, Reply


class TweetInfo:

    def __init__(self, tweet, tweet_like, reply):
        self.tweet = tweet
        self.number_tweet_likes = tweet_like
        self.reply = reply


def index(request):
    tweet_list = (Tweet.objects.all()).order_by('-time_tweeted')
    tweet_infos = []
    for tweet in tweet_list:
        reply = tweet.reply_set.all()
        tweet_info = TweetInfo(tweet, tweet.like_set.all().count(), reply)
        tweet_infos.append(tweet_info)
    context = {
        'tweet_info_list': tweet_infos,
    }
    template = loader.get_template('tweeter/index.html')
    return HttpResponse(template.render(context, request))


def add_tweet(request):
    current_user = request.user
    user_id = current_user.id
    current_time = timezone.now()
    new_tweet = Tweet.objects.create(user_id=user_id, tweet_text=request.POST['tweet_text'], time_tweeted=current_time)
    new_tweet.save()
    return HttpResponseRedirect(reverse('tweeter:index'))


def like_tweet(request, tweet_id):
    new_like, created = Like.objects.get_or_create(user=request.user, tweet_id=tweet_id)
    if not created:
        new_like.delete()
        return HttpResponseRedirect(reverse('tweeter:index'))
    else:
        new_like.save()
        return HttpResponseRedirect(reverse('tweeter:index'))


def reply_tweet(request, tweet_id):
    current_user = request.user
    user_id = current_user.id
    new_reply = Reply.objects.create(user_id=user_id, tweet_id=tweet_id, reply_text=request.POST['reply_text'])
    new_reply.save()
    return HttpResponseRedirect(reverse('tweeter:index'))


def people(request):
    user_list = User.objects.all()
    context = {
        'user_list': user_list,
    }
    template = loader.get_template('tweeter/people.html')
    return HttpResponse(template.render(context, request))

from itertools import chain

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
from django.utils import timezone

# Create your views here.
from tweeter.models import Tweet, Like, Reply, Follow


class TweetInfo:

    def __init__(self, tweet, tweet_like, reply, is_liked):
        self.tweet = tweet
        self.number_tweet_likes = tweet_like
        self.reply = reply
        self.is_liked = is_liked


def index(request):
    user_follow_list = [x.user_followed_id for x in Follow.objects.filter(user_follow_id=request.user.id)]
    tweet_list = []
    for x in user_follow_list:
        if Tweet.objects.filter(user_id=x):
            tweet_list.append(Tweet.objects.filter(user_id=x))
    all_tweet_list = Tweet.objects.filter(user_id=request.user.id)
    for x in range(0, len(tweet_list)):
        all_tweet_list = chain(all_tweet_list, tweet_list[x])
    all_tweet_list = list(all_tweet_list)
    all_tweet_list.sort(key=lambda x: x.time_tweeted, reverse=True)
    tweet_infos = []
    for tweet in all_tweet_list:
            is_liked = tweet.like_set.filter(user_id=request.user.id)
            reply = (tweet.reply_set.all()).order_by('time_reply')
            tweet_info = TweetInfo(tweet, tweet.like_set.all().count(), reply, is_liked)
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

    class FollowInfo:
        def __init__(self, user_to_display, number_of_following, number_of_follower, is_followed):
            self.user_to_display = user_to_display
            self.number_of_following = number_of_following
            self.number_of_follower = number_of_follower
            self.is_followed = is_followed
    user_list = User.objects.all()
    user_with_follow_info_list = []
    for u in user_list:
        is_followed = Follow.objects.filter(user_follow_id=request.user.id, user_followed_id=u.id)
        user_with_follow_info = FollowInfo(u, Follow.objects.filter(user_follow_id=u.id).count(), Follow.objects.filter(user_followed_id=u.id).count(), is_followed)
        user_with_follow_info_list.append(user_with_follow_info)
    context = {
        'user_with_follow_info_list': user_with_follow_info_list,
    }
    template = loader.get_template('tweeter/people.html')
    return HttpResponse(template.render(context, request))


def follow(request, user_followed_id):
    current_user = request.user
    new_follow, created = Follow.objects.get_or_create(user_follow_id=current_user.id, user_followed_id=user_followed_id)
    if not created:
        new_follow.delete()
        return HttpResponseRedirect(reverse('tweeter:people'))
    else:
        new_follow.save()
        return HttpResponseRedirect(reverse('tweeter:people'))

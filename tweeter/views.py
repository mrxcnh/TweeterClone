from itertools import chain
from django.views.generic import ListView, FormView, TemplateView
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from tweeter.forms import ReplyForm, TweetForm, ProfileForm
from tweeter.models import Tweet, Like, Reply, Follow, UserProfile


class TweetInfo:

    def __init__(self, tweet, tweet_like, reply, is_liked):
        self.tweet = tweet
        self.number_tweet_likes = tweet_like
        self.reply = reply
        self.is_liked = is_liked


class IndexView(TemplateView):
    template_name = 'tweeter/index.html'

    def get(self, request, *args, **kwargs):
        reply_form = ReplyForm()
        tweet_form = TweetForm()
        user_follow_list = Follow.objects.filter(
            user_follow_id=request.user.id
        ).values_list(
            'user_followed_id',
            flat=True
        )
        user_follow_list = list(user_follow_list)
        user_follow_list.append(request.user.id)
        all_tweet_list = Tweet.objects.filter(user_id__in=user_follow_list).order_by('-time_tweeted')
        tweet_infos = []
        for tweet in all_tweet_list:
            is_liked = tweet.like_set.filter(user_id=self.request.user.id)
            reply = (tweet.reply_set.all()).order_by('time_reply')
            tweet_info = TweetInfo(tweet, tweet.like_set.all().count(), reply, is_liked)
            tweet_infos.append(tweet_info)
        return render(request, self.template_name,
                      {'reply_form': reply_form, 'tweet_info_list': tweet_infos, 'tweet_form': tweet_form, })


class AddTweetView(View):

    def post(self, request):
        current_user = request.user
        user_id = current_user.id
        new_tweet = Tweet.objects.create(user_id=user_id, tweet_text=request.POST['tweet_text'])
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


def like_tweet1(request, tweet_id):
    new_like, created = Like.objects.get_or_create(user=request.user, tweet_id=tweet_id)
    if not created:
        new_like.delete()
        return HttpResponseRedirect(reverse('tweeter:user_profile', args=(request.user.id,)))
    else:
        new_like.save()
        return HttpResponseRedirect(reverse('tweeter:user_profile', args=(request.user.id,)))


class ReplyTweetView(FormView):
    template_name = 'tweeter/index.html'
    form_class = ReplyForm

    def form_valid(self, form):
        current_user = self.request.user
        user_id = current_user.id
        new_reply = Reply.objects.create(user_id=user_id, tweet_id=self.kwargs['tweet_id'],
                                         reply_text=self.request.POST['reply'])
        new_reply.save()
        return HttpResponseRedirect(reverse('tweeter:index'))

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('tweeter:index'))


class ReplyTweetView1(FormView):
    template_name = 'tweeter/user_profile.html'
    form_class = ReplyForm

    def form_valid(self, form):
        current_user = self.request.user
        user_id = current_user.id
        new_reply = Reply.objects.create(user_id=user_id, tweet_id=self.kwargs['tweet_id'],
                                         reply_text=self.request.POST['reply'])
        new_reply.save()
        return HttpResponseRedirect(reverse('tweeter:user_profile', args=(user_id,)))

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('tweeter:user_profile', args=(self.request.user.id,)))


class EditUserProfileView(FormView):
    template_name = 'tweeter/user_profile.html'
    form_class = ProfileForm

    def form_valid(self, form):
        current_user = self.request.user
        user_id = current_user.id
        user_profile = UserProfile.objects.get(user_id=user_id)
        user_profile.bio = self.request.POST['bio']
        user_profile.location = self.request.POST['location']
        user_profile.website = self.request.POST['website']
        user_profile.save()
        return HttpResponseRedirect(reverse('tweeter:user_profile', args=(user_id,)))


class FollowInfo:
    def __init__(self, user_to_display, number_of_following, number_of_follower, is_followed):
        self.user_to_display = user_to_display
        self.number_of_following = number_of_following
        self.number_of_follower = number_of_follower
        self.is_followed = is_followed


class FollowerView(ListView):
    template_name = 'tweeter/people.html'
    model = User, Follow
    context_object_name = 'user_with_follow_info_list'

    def get_queryset(self):
        user_list = User.objects.all()
        user_with_follow_info_list = []
        for u in user_list:
            is_followed = Follow.objects.filter(user_follow_id=self.request.user.id, user_followed_id=u.id)
            user_with_follow_info = FollowInfo(u, Follow.objects.filter(user_follow_id=u.id).count(),
                                               Follow.objects.filter(user_followed_id=u.id).count(), is_followed)
            user_with_follow_info_list.append(user_with_follow_info)
        return user_with_follow_info_list


def follow(request, user_followed_id):
    current_user = request.user
    new_follow, created = Follow.objects.get_or_create(user_follow_id=current_user.id,
                                                       user_followed_id=user_followed_id)
    if not created:
        new_follow.delete()
        return HttpResponseRedirect(reverse('tweeter:people'))
    else:
        new_follow.save()
        return HttpResponseRedirect(reverse('tweeter:people'))


class UserProfileView(ListView):
    template_name = 'tweeter/user_profile.html'
    model = UserProfile
    context_object_name = 'user_profiles'

    def get_queryset(self):
        user_profiles = UserProfile.objects.filter(user_id=self.kwargs['user_id'])
        return user_profiles


class UserInfo:

    def __init__(self, id, bio, location, website, tweet_count, following_count, follower_count, like_count):
        self.id = id
        self.bio = bio
        self.location = location
        self.website = website
        self.tweet_count = tweet_count
        self.following_count = following_count
        self.follower_count = follower_count
        self.like_count = like_count


class UserProfileView(TemplateView):
    template_name = 'tweeter/user_profile.html'

    def get(self, request, *args, **kwargs):
        reply_form = ReplyForm()
        tweet_form = TweetForm()
        all_tweet_list = Tweet.objects.filter(user_id=self.kwargs['user_id'])
        all_tweet_list = list(all_tweet_list)
        all_tweet_list.sort(key=lambda x: x.time_tweeted, reverse=True)
        tweet_infos = []
        for tweet in all_tweet_list:
            is_liked = tweet.like_set.filter(user_id=self.request.user.id)
            reply = (tweet.reply_set.all()).order_by('time_reply')
            tweet_info = TweetInfo(tweet, tweet.like_set.all().count(), reply, is_liked)
            tweet_infos.append(tweet_info)
        tweet_count = len(tweet_infos)
        following_count = Follow.objects.filter(user_follow_id=self.kwargs['user_id']).count()
        id = self.kwargs['user_id']
        follower_count = Follow.objects.filter(user_followed_id=self.kwargs['user_id']).count()
        like_count = Like.objects.filter(user_id=self.kwargs['user_id']).count()
        bio = UserProfile.objects.get(user_id=self.kwargs['user_id']).bio
        location = UserProfile.objects.get(user_id=self.kwargs['user_id']).location
        website = UserProfile.objects.get(user_id=self.kwargs['user_id']).website
        user_info = UserInfo(id, bio, location, website, tweet_count, following_count, follower_count, like_count)
        profile_form = ProfileForm(initial={'bio': user_info.bio,
                                            'location': user_info.location, 'website': user_info.website})
        return render(request, self.template_name, {'reply_form': reply_form,
                                                    'tweet_info_list': tweet_infos,
                                                    'tweet_form': tweet_form,
                                                    'user_info': user_info,
                                                    'profile_form': profile_form})

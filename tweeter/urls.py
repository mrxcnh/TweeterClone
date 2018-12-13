from django.urls import path

from tweeter import views

app_name = 'tweeter'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add_tweet/', views.AddTweetView.as_view(), name='add_tweet'),
    path('<int:tweet_id>/like_tweet/', views.like_tweet, name='like_tweet'),
    path('<int:tweet_id>/like_tweet1/', views.like_tweet1, name='like_tweet1'),
    path('people/', views.FollowerView.as_view(), name='people'),
    path('<int:tweet_id>/reply_tweet/', views.ReplyTweetView.as_view(), name='reply_tweet'),
    path('<int:tweet_id>/reply_tweet1/', views.ReplyTweetView1.as_view(), name='reply_tweet1'),
    path('<int:user_followed_id>/follow/', views.follow, name='follow_user'),
    path('<int:user_id>/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('<int:user_id>/edit_profile/', views.EditUserProfileView.as_view(), name='edit_user_profile')
]

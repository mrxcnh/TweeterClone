from django.urls import path

from tweeter import views

app_name = 'tweeter'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_tweet/', views.add_tweet, name='add_tweet'),
    path('<int:tweet_id>/like_tweet/', views.like_tweet, name='like_tweet'),
    path('people/', views.people, name='people'),
    path('<int:tweet_id>/reply_tweet/', views.reply_tweet, name='reply_tweet'),
    path('<int:user_followed_id>/follow/', views.follow, name='follow_user'),
]

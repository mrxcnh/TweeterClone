from django.urls import path

from tweeter import views

app_name = 'tweeter'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add_tweet/', views.add_tweet, name='add_tweet'),
]

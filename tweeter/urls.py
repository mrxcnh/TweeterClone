from django.urls import path

from tweeter import views

app_name = 'tweeter'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]

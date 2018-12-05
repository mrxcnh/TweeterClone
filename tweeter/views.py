from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

# Create your views here.
from tweeter.models import Tweet


class IndexView(generic.ListView):
    template_name = 'tweeter/index.html'

    def get_queryset(self):
        return Tweet.objects.all()

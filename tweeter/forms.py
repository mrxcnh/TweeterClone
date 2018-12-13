from django import forms


class ReplyForm(forms.Form):
    reply = forms.CharField(max_length=1000, required=True)


class TweetForm(forms.Form):
    tweet_text = forms.CharField(max_length=1000, required=True)


class ProfileForm(forms.Form):
    bio = forms.CharField(max_length=500)
    location = forms.CharField(max_length=500)
    website = forms.URLField()

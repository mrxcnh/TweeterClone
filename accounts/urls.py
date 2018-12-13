from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup2/', views.SignupUserView.as_view(), name='signup2'),
    path('login2/', views.LoginView.as_view(), name='login2'),
    path(r'ajax/validate_username/$', views.validate_username, name='validate_username')
]

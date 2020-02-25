from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account'

urlpatterns = [
    # login user
    path('login/', auth_views.LoginView.as_view(), name='login'),

    # logout user
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

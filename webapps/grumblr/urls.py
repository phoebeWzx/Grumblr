from django.urls import path
from django.contrib import auth
from django.contrib.auth import views
from . import views
from grumblr.forms import *

urlpatterns = [
        path('', views.global_stream, name='home'),
        path('login', auth.views.LoginView.as_view(template_name='grumblr/LoginPage.html', form_class=LoginForm, redirect_authenticated_user=True), name='login'),
        path('logout', auth.views.LogoutView.as_view(template_name='grumblr/LoginPage.html', next_page='login'), name='logout'),


        path('register', views.register, name='register'),
        path('profile/<username>', views.profile, name='profile'),
        path('profile/<username>/follow', views.follow, name='follow'),
        path('profile/<username>/unfollow', views.unfollow, name='unfollow'),

        path('editProfile/<username>', views.update_profile, name='editProfile'),

        path('change_password/<username>', views.change_password, name='change-password'),
        path('reset_password', views.reset_password, name='reset-password'),
        path('reset_confirm/<username>/<token>', views.reset_confirm, name='reset-confirm'),
        path('password_confirm/<username>', views.password_confirm, name='password-confirm'),
        path('follower_stream', views.follow_stream, name='follower-stream'),
        path('global', views.global_stream, name='global'),
        path('add_post', views.add_post, name='post'),
        path('add_comment/<post_id>', views.add_comment, name="comment"),
        path('register_confirm/<username>/<token>', views.register_confirm, name='confirm'),

        path('get_post', views.get_post, name='get-post'),
        path('get_comment/<post_id>', views.get_comment, name='get-comment')
]


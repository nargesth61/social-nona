from django.urls import path ,include
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('logout', views.logout, name='logout'),
    path('like-post', views.like_post, name='like-post'),
    path('settings', views.settings, name='settings'),
    path('upload',views.upload,name='upload'),
    ]
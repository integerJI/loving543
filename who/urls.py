from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('join/', views.signup, name='join'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.userinfo, name='mypage'),
    path('userpage/<str:writer>', views.user_select_info, name='userpage'),
    path('profile_update', views.ProfileUpdateView.as_view(), name='profile_update'),
]

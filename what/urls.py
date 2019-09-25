from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('post', views.post, name="post"),
    url(r'^(?P<memokey>[0-9]+)/modify/$', views.modify, name='modify_memo'),
    url(r'^(?P<memokey>[0-9]+)/delete/$', views.delete, name='delete_memo'),
    url(r'^like/$', views.like, name='like'),
    url(r'^(?P<memokey>[0-9]+)/comment_write/$', views.comment_write, name='comment_write'),
    path('<int:memo_pk>/<int:pk>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('<int:memo_id>/', views.detail, name="detail"),
    url(r'^explore/tags/(?P<tag>\w+)/$', views.index, name='post_search'),
    url(r'^explore/tags2/(?P<tag2>\w+)/$', views.index, name='post_search'),
    path('search/', views.search, name="search"),
]

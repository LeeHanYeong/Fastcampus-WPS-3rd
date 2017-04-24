from django.conf.urls import url
from . import views
from . import ajax

urlpatterns = [
    url(r'^$', views.album_list, name='album_list'),
    url(r'^album/add/$', views.album_add, name='album_add'),
    url(r'^album/(?P<pk>[0-9]+)/$', views.album_detail, name='album_detail'),
    url(r'^album/(?P<album_pk>[0-9]+)/photo/add/$', views.photo_add, name='photo_add'),
    url(r'^album/(?P<album_pk>[0-9]+)/photo/multi/add/$', views.photo_multi_add, name='photo_multi_add'),
    url(r'^photo/(?P<pk>[0-9]+)/$', views.photo_detail, name='photo_detail'),
    url(r'^photo/(?P<pk>[0-9]+)/(?P<like_type>\w+)/$', views.photo_like, name='photo_like'),

    url(r'^ajax/photo/(?P<pk>[0-9]+)/(?P<like_type>\w+)/$', ajax.photo_like, name='ajax_photo_like'),
]
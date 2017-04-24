from django.conf.urls import url
from .. import apis

urlpatterns = [
    url(r'^photo/add/$', apis.photo_add, name='photo_add'),
    url(r'^photo/$', apis.photo_list, name='photo_list'),
    url(r'^(?P<photo_pk>[0-9]+)/comment/add/$', apis.comment_add, name='comment_add'),
]

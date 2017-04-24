from django.conf.urls import url
from .. import apis
from ..apis import PhotoViewSet


photo_list = PhotoViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
photo_detail = PhotoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})


urlpatterns = [
    # APIView 사용
    # url(r'^photo/$', apis.PhotoList.as_view(), name='photo_list'),

    # Mixin 사용
    # url(r'^photo/$', apis.PhotoListMixinView.as_view(), name='photo_list'),

    # ViewSet사용
    url(r'^photo/$', photo_list, name='photo_list'),
    url(r'^photo/(?P<pk>[0-9]+)/$', photo_detail, name='photo_detail'),

    ### PhotoComment
    # APIView 사용
    url(r'^photo/comment/$', apis.PhotoCommentView.as_view(), name='photo_comment_list_default'),

    url(r'^(?P<photo_pk>[0-9]+)/comment/add/$', apis.comment_add, name='comment_add'),
]

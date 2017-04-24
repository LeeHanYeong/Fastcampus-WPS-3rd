import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from photo.serializers import PhotoSerializer, PhotoCommentSerializer
from .models import Photo, PhotoComment

User = get_user_model()


class PhotoList(APIView):
    def get(self, request):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoListMixinView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('author', )



    # def list(self, request, *args, **kwargs):
    #     return_data = None
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         cache_key = 'photo_list_%s' % page
    #         cached_data = cache.get(cache_key)
    #         if cached_data:
    #             return_data = cached_data
    #         else:
    #             serializer = self.get_serializer(page, many=True)
    #             return_data = serializer.data
    #             cache.set(cache_key, return_data)
    #         return self.get_paginated_response(return_data)
    #
    #     cache_key = 'photo_list'
    #     cached_data = cache.get(cache_key)
    #     if cached_data:
    #         return Response(cached_data)
    #     else:
    #         serializer = self.get_serializer(queryset, many=True)
    #         cache.set(cache_key, serializer.data)
    #         return Response(serializer.data)
    #

def photo_list(request):
    photos = Photo.objects.all()
    data = {
        'photos': [photo.to_dict() for photo in photos],
    }
    return HttpResponse(
        json.dumps(data),
        content_type='application/json'
    )


"""
Comment add API만들어보기
0. CommentSerializer 구현
1. APIView상속받아 post에 구현
2. mixins를 사용해서 create에 구현
3. ViewSet을 사용
"""


class PhotoCommentView(APIView):
    # def get(self, request, *args, **kwargs):
    #     print(kwargs)
    #     if 'photo_pk' in kwargs:
    #         photo = get_object_or_404(Photo, pk=kwargs.get('photo_pk'))
    #         comments = PhotoComment.objects.filter(photo=photo)
    #     else:
    #         comments = PhotoComment.objects.all()
    #     serializer = PhotoCommentSerializer(comments, many=True)
    #     return Response(serializer.data)
    def post(self, request):
        serializer = PhotoCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def photo_add(request):
    data = request.POST
    files = request.FILES

    user_id = data['user_id']
    content = data['content']
    image = files['photo']

    author = User.objects.get(id=user_id)
    photo = Photo.objects.create(
        image=image,
        author=author,
        content=content
    )
    return HttpResponse(
        json.dumps(photo.to_dict()),
        content_type='application/json'
    )


@csrf_exempt
def comment_add(request, photo_pk):
    data = request.POST

    user_id = data['user_id']
    content = data['content']

    author = User.objects.get(id=user_id)
    photo = Photo.objects.get(id=photo_pk)

    photo_comment = PhotoComment.objects.create(
        photo=photo,
        author=author,
        content=content
    )
    return HttpResponse(
        json.dumps(photo_comment.to_dict()),
        content_type='application/json'
    )
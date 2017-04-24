from django.db import models
from django.conf import settings
from member.models import MyUser as User
"""
Album
    title : CharField
    owner : ForeignKey
    description : CharField

Photo
    Album : ForeignKey
    owner : ForeignKey
    title : CharField
    description : CharField
    img : ImageField

Photo좋아요를 구현하고싶으면 어떻게해야될까요?
좋아요에는 해당 Photo, User, 좋아요누른시간이 기록됩니다
"""


class Album(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.CharField(max_length=80, blank=True)


class Photo(models.Model):
    album = models.ForeignKey(Album)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=80, blank=True)
    img = models.ImageField(upload_to='photo')
    # M2M Field를 사용해서 좋아요 내용을 거치도록 합니다 (중간자 모델)
    # https://docs.djangoproject.com/en/1.10/topics/db/models/#intermediary-manytomany
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PhotoLike', related_name='photo_set_like_users')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PhotoDislike', related_name='photo_set_dislike_users')


class PhotoLike(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class PhotoDislike(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

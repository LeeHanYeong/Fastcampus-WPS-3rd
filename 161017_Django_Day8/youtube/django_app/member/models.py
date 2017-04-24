from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, User


# 기본 장고 유저(auth.User)의 Manager와 User를 상속받아 사용합니다
class YoutubeUserManager(UserManager):
    pass


class YoutubeUser(AbstractUser):
    nickname = models.CharField(max_length=24)

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'

    def __str__(self):
        return self.username

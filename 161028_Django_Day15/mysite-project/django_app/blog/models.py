from datetime import datetime
from django.db import models
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apis.mail import send_mail


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


# 댓글을 저장하는 데이터베이스 모델
class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        # recipient_list = [self.post.author.email]
        # title = '{} 글에 댓글이 달렸습니다'.format(self.post.title)
        # content = '{}에 {}내용이 달렸네요'.format(
        #     self.created_date.strftime('%Y.%m.%d %H:%M'),
        #     self.content
        # )
        # send_mail(title, content)



# post_save.connect(send_comment_mail, sender=Comment)
from django.db import models
from django.conf import settings

__all__ = [
    'Photo',
    'PhotoTag',
    'PhotoComment',
    'PhotoLike',
]


class Photo(models.Model):
    image = models.ImageField(upload_to='photo', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(blank=True)
    tags = models.ManyToManyField('PhotoTag', blank=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PhotoLike',
        related_name='photo_set_like_users'
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pk', )

    def __str__(self):
        return '%s (author:%s)' % (
            self.content,
            self.author.get_full_name()
        )

    def to_dict(self):
        ret = {
            'id': self.id,
            'image': self.image.url,
            'author': self.author.id,
            'content': self.content,
            'commentList': [comment.to_dict() for comment in self.photocomment_set.all()],
        }
        return ret


class PhotoTag(models.Model):
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)


class PhotoComment(models.Model):
    photo = models.ForeignKey(Photo)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()

    def to_dict(self):
        ret = {
            'id': self.id,
            'photo': self.photo.id,
            'author': self.author.id,
            'content': self.content,
        }
        return ret


class PhotoLike(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.conf import settings
from mysite.utils.models import BaseModel
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


class Album(BaseModel):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.CharField(max_length=80, blank=True)


class Photo(BaseModel):
    album = models.ForeignKey(Album)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=80, blank=True)
    img = models.ImageField(upload_to='photo')
    img_thumbnail = models.ImageField(upload_to='photo/thumbnail', blank=True)
    # M2M Field를 사용해서 좋아요 내용을 거치도록 합니다 (중간자 모델)
    # https://docs.djangoproject.com/en/1.10/topics/db/models/#intermediary-manytomany
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PhotoLike', related_name='photo_set_like_users')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PhotoDislike', related_name='photo_set_dislike_users')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image_changed = False

        # save전, img필드의 내용이 변했는지 확인
        # 기존에 DB에 저장되어있을 경우에만 지정(self.pk가 없을경우 에러)
        if self.pk:
            ori = Photo.objects.get(pk=self.pk)
            if ori.img != self.img:
                image_changed = True

        # img는 있는데 img_thumbnail은 없을 경우
        if self.img and not self.img_thumbnail:
            image_changed = True

        super().save(*args, **kwargs)
        if image_changed:
            self.make_thumbnail()

    def make_thumbnail(self):
        import os
        from PIL import Image, ImageOps
        from io import BytesIO
        from django.core.files.base import ContentFile
        from django.core.files.storage import default_storage

        size = (300, 300)
        # Default storage에서 FileField내용 읽어오기
        f = default_storage.open(self.img)
        print('f : %s' % f)

        # Image.open으로 파일을 Image인스턴스화 (image)
        image = Image.open(f)
        # Image.format은 JPEG, PNG, BMP등 포맷정보를 나타냄
        ftype = image.format
        print('ftype : %s' % ftype)

        # ImageOps.fit메서드를 이용해서 썸네일이미지 생성
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # 기존에 있던 img의 경로와 확장자를 가져옴
        path, ext = os.path.splitext(self.img.name)
        name = os.path.basename(path)

        # 기존파일명_thumb.확장자 형태가 됨
        thumbnail_name = '%s_thumb%s' % (name, ext)

        # 임시 파일로 취급되는 객체 생성
        temp_file = BytesIO()
        image.save(temp_file, ftype)
        temp_file.seek(0)

        # img_thumbnail필드에 해당 파일내용을 저장
        # Django의 FileField에 내용을 저장할때는 ContentFile형식이어야 함
        content_file = ContentFile(temp_file.read())
        self.img_thumbnail.save(thumbnail_name, content_file)

        # 열었던 파일 닫아줌
        temp_file.close()
        content_file.close()
        f.close()
        return True







class PhotoLike(BaseModel):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class PhotoDislike(BaseModel):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

from django.db import models
from django.contrib.auth.models import \
    AbstractBaseUser, AbstractUser, \
    BaseUserManager, PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            last_name,
            first_name,
            nickname,
            password=None):
        user = self.model(
            email=email,
            last_name=last_name,
            first_name=first_name,
            nickname=nickname
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self,
            email,
            last_name,
            first_name,
            nickname,
            password):
        user = self.model(
            email=email,
            last_name=last_name,
            first_name=first_name,
            nickname=nickname
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def create_facebook_user(self, user_info):
        user = self.model(
            email=user_info['email'],
            last_name=user_info.get('last_name', ''),
            first_name=user_info.get('first_name', ''),
            is_facebook_user=True,
            facebook_id=user_info['id'],
            img_profile_url=user_info['picture']['data']['url'],
        )
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('이메일', max_length=100, unique=True)
    last_name = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=20, blank=True)
    nickname = models.CharField(max_length=24)
    phone_number = models.CharField(max_length=15, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    # Facebook User
    is_facebook_user = models.BooleanField(default=False)
    facebook_id = models.CharField(max_length=200, blank=True)
    img_profile_url = models.URLField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('last_name', 'first_name', 'nickname', )

    objects = MyUserManager()

    def get_full_name(self):
        return '%s%s' % (self.last_name, self.first_name)

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        # save시 전화번호에 '-'가 들어가있으면 없애준다
        if '-' in self.phone_number:
            self.phone_number = self.phone_number.replace('-', '')
        super().save(*args, **kwargs)



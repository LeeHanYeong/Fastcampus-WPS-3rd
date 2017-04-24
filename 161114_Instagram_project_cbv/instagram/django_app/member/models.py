from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, UserManager


class MyUserManager(UserManager):
    pass


class MyUser(AbstractUser):
    img_profile = models.ImageField(
        upload_to='user',
        blank=True
    )
    following_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relationship',
        related_name='follower_users'
    )
    block_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='user_set_block'
    )
    # like_photos = models.ManyToManyField(
    #     Photo,
    #     through=PhotoLike,
    #     related_name='user_set_like_photos'
    # )

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '%s%s' % (self.last_name, self.first_name)

    def friends(self):
        """
        자신이 follow한 유저들 중에 자신을 following_users로 가지고 있는 유저 목록을 리턴
        :return: User Queryset
        """
        return self.following_users.filter(following_users=self)

    def follow(self, user):
        """
        주어진 User Instance를 이용해서 Following관계를 만들어준다
        이 때 get_or_create함수를 이용해서 중복이 발생하지 않도록 한다
        """
        instance, created = Relationship.objects.get_or_create(
            follower=self,
            followee=user
        )
        return instance

    def unfollow(self, user):
        """
        주어진 User Instance를 자신의 following_users에서 제거한다
        """
        Relationship.objects.filter(
            follower=self,
            followee=user
        ).delete()

    def block(self, user):
        self.block_users.add(user)

    def unblock(self, user):
        self.block_users.remove(user)

    def is_friends(self, user):
        """
        주어진 User Instance가 self.friends()메서드를 통해 돌아온 UserList에 속하는지 리턴
        """
        if user in self.friends():
            return True
        return False


class Relationship(models.Model):
    follower = models.ForeignKey(MyUser, related_name='relationship_set_follower')
    followee = models.ForeignKey(MyUser, related_name='relationship_set_followee')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')

    def __str__(self):
        return 'Relation(Follower(%s), Followee(%s))' % (
            self.follower.get_full_name(),
            self.followee.get_full_name(),
        )

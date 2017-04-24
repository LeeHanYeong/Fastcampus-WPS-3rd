from django.db.models import Q
from django.test import TestCase, LiveServerTestCase
from .models import MyUser, Relationship


class FollowTest(LiveServerTestCase):
    def create_user(self, username, last_name, first_name):
        return MyUser.objects.create_user(
            username=username,
            last_name=last_name,
            first_name=first_name,
        )

    def test_create_user(self):
        print('test_create_user')
        u1 = self.create_user('u1', '방', '민아')
        u2 = self.create_user('u2', '이', '한영')
        u3 = self.create_user('u3', '박', '성환')

    def test_follow_user(self):
        u1 = self.create_user('u1', '방', '민아')
        u2 = self.create_user('u2', '이', '한영')
        u3 = self.create_user('u3', '박', '성환')

        u1.follow(u2)
        u1.unfollow(u2)

        u2.follow(u1)
        u3.follow(u2)
        u3.follow(u1)

        # print(u1.following_users.all())
        # print(u2.following_users.all())
        # print(u3.following_users.all())
        #
        # print(u1.follower_users.all())

    # def test_follow_unique(self):
    #     u1 = self.create_user('u1', '방', '민아')
    #     u2 = self.create_user('u2', '이', '한영')
    #
    #     u1.follow(u2)
    #     u1.follow(u2)

    def test_friends(self):
        u1 = self.create_user('u1', '방', '민아')
        u2 = self.create_user('u2', '이', '한영')
        u3 = self.create_user('u3', '박', '성환')

        # 민아는 한영을 팔로우
        u1.follow(u2)

        # 한영은 민아와 성환을 팔로우
        u2.follow(u1)
        u2.follow(u3)

        # 성환은 한영과 민아를 팔로우
        u3.follow(u2)

        print(u2.relationship_set_follower.all())
        print(Relationship.objects.filter(follower=u2))

        # 민아의 친구들 목록
        u1_friends = u1.following_users.filter(following_users=u1)

        # 한영의 친구들 목록
        u2_friends = u2.following_users.filter(following_users=u2)

        # 성환의 친구들 목록
        u3_friends = u3.following_users.filter(following_users=u3)

        print(u1_friends)
        print(u2_friends)
        print(u3_friends)

        print(u1.is_friends(u2))
        print(u2.is_friends(u1))
        print(u1.is_friends(u3))
from django.contrib.auth import get_user_model
User = get_user_model()
# 아래와 동일
# from member.models import MyUser as User


class FacebookBackend:
    def authenticate(self, user_info, token=None):
        try:
            user = User.objects.get(facebook_id=user_info.get('id'))
            return user
        except User.DoesNotExist:
            user = User.objects.create_facebook_user(user_info)
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

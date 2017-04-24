from rest_framework import serializers

from member.serializers import UserSerializer
from .models import Photo, PhotoComment


class PhotoCommentSerializer(serializers.ModelSerializer):
    """
    UserSerializer를 구현하고, author field를 Nested relation으로 나타냄
    author필드에서 UserSerializer를 사용하도록 설정
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = PhotoComment
        fields = (
            'id',
            'photo',
            'author',
            'content',
        )


class PhotoSerializer(serializers.ModelSerializer):
    comment_list = PhotoCommentSerializer(
        many=True,
        read_only=True,
        source='photocomment_set',
    )

    class Meta:
        model = Photo
        fields = (
            'id',
            'author',
            'content',
            'image',
            'comment_list',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # ret['comment_list'] = PhotoCommentSerializer(
        #     instance.photocomment_set.all(),
        #     many=True).data
        return ret



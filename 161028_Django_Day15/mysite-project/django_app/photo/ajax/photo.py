import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..models import Photo, PhotoLike, PhotoDislike

__all__ = [
    'photo_like',
]


@require_POST
@csrf_exempt
def photo_like(request, pk, like_type='like'):
    photo = get_object_or_404(Photo, pk=pk)
    album = photo.album
    next_path = request.GET.get('next')
    like_model = PhotoLike if like_type == 'like' else PhotoDislike
    opposite_model = PhotoDislike if like_type == 'like' else PhotoLike

    user_like_exist = like_model.objects.filter(
        user=request.user,
        photo=photo
    )

    is_delete = False
    # 요청한 유저가 이미 좋아요(또는 싫어요)를 했는가?
    if user_like_exist.exists():
        user_like_exist.delete()
        is_delete = True
    # 이미 누르지 않은 경우, 좋아요 처리를 해준다
    else:
        like_model.objects.create(
            user=request.user,
            photo=photo
        )
        # 근데 이사람이 싫어요(또는 반대모델)를 눌러놨을 경우
        # 해당하는 경우를 지워준다
        opposite_model.objects.filter(
            user=request.user,
            photo=photo
        ).delete()
    ret = {
        'like_count': photo.like_users.count(),
        'dislike_count': photo.dislike_users.count(),
        'user_like': False,
        'user_dislike': False,
        # 'user_like': True if photo.like_users.filter(pk=request.user.pk).exists() else False,
        # 'user_dislike': True if photo.dislike_users.filter(pk=request.user.pk).exists() else False,
    }
    if not is_delete:
        ret['user_like'] = True if like_type == 'like' else False
        ret['user_dislike'] = True if like_type != 'like' else False

    # return HttpResponseBadRequest(json.dumps(ret), content_type='application/json')
    return HttpResponse(json.dumps(ret), content_type='application/json')
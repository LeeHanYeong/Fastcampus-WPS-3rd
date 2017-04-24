from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from ..models import Album, Photo, PhotoLike, PhotoDislike
from ..forms import PhotoForm, MultiPhotoForm

__all__ = [
    'photo_add',
    'photo_multi_add',
    'photo_detail',
    'photo_like',
]


@login_required
def photo_add(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            # img = request.FILES['img']
            img = form.cleaned_data['img']
            Photo.objects.create(
                album=album,
                owner=request.user,
                title=title,
                description=description,
                img=img,
            )
            return redirect('photo:album_detail', pk=album_pk)
    else:
        form = PhotoForm()
    context = {
        'form': form,
    }
    return render(request, 'photo/photo_add.html', context)


@login_required
def photo_multi_add(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    if request.method == 'POST':
        form = MultiPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            files = request.FILES.getlist('img')
            for index, file in enumerate(files):
                Photo.objects.create(
                    album=album,
                    owner=request.user,
                    title='%s(%s)' % (title, index+1),
                    description='%s(%s)' % (description, index+1),
                    img=file,
                )
            return redirect('photo:album_detail', pk=album_pk)
    else:
        form = MultiPhotoForm()
    context = {
        'form': form,
    }
    return render(request, 'photo/photo_multi_add.html', context)


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    context = {
        'photo': photo,
    }
    return render(request, 'photo/photo_detail.html', context)


@login_required
@require_POST
def photo_like(request, pk, like_type='like'):
    """
    1. 요청한 유저가 이 사진에 좋아요(또는 싫어요)를 눌렀는가?
    2. 이미 좋아요를 눌렀는데 다시 좋아요를 누른 경우
    3. 이미 좋아요를 눌렀는데 싫어요를 누른 경우
    """
    photo = get_object_or_404(Photo, pk=pk)
    album = photo.album
    next_path = request.GET.get('next')
    like_model = PhotoLike if like_type == 'like' else PhotoDislike
    opposite_model = PhotoDislike if like_type == 'like' else PhotoLike

    user_like_exist = like_model.objects.filter(
        user=request.user,
        photo=photo
    )
    # 요청한 유저가 이미 좋아요(또는 싫어요)를 했는가?
    if user_like_exist.exists():
        user_like_exist.delete()

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

    if next_path:
        return redirect(next_path)
    else:
        return redirect('photo:album_detail', pk=album.pk)
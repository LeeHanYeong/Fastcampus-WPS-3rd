from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Album
from ..forms import AlbumForm

__all__ = [
    'album_list',
    'album_add',
    'album_detail',
]


def album_list(request):
    albums = Album.objects.all()
    context = {
        'albums': albums,
    }
    return render(request, 'photo/album_list.html', context)


def album_add(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            Album.objects.create(
                title=title,
                description=description,
                owner=request.user,
            )
            return redirect('photo:album_list')
    else:
        form = AlbumForm()
    context = {
        'form': form,
    }
    return render(request, 'photo/album_add.html', context)


def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    photo_list = album.photo_set.all()
    paginator = Paginator(photo_list, 4)

    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    context = {
        'album': album,
        'photos': photos,
    }
    # template_file = 'photo/album_detail.html'
    template_file = 'photo/ajax_album_detail.html'
    return render(request, template_file, context)

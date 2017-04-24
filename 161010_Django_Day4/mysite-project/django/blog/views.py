from django.shortcuts import render, HttpResponse
from django.utils import timezone
from django.db.models import Q
from .models import Post

# 같은 의미
# from blog.models import Post


def post_list(request):
    # posts = Post.objects\
    #     # .filter(published_date__lte=timezone.now())\
    #     .order_by('published_date')

    # published_date의 값이 데이터베이스에서 NULL일 경우
    posts = Post.objects \
        .filter(
            Q(published_date__lte=timezone.now()) |
            Q(published_date=None)
        ).order_by('published_date')
    return render(request, 'blog/post_list.html', {'post_list': posts, 'title': '타이틀 변수는 title키를 이용해서 접근'})

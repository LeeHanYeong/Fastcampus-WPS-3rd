from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from .models import Post, Comment
from django.contrib.auth.models import User

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


def post_detail(request, pk):
    """
    post_detail뷰(지금 작업중인 뷰)에서 전달받은 pk를 이용해서
    pk값(id값)이 전달받은 pk인 Post객체를 Query하여 post라는 변수에 할당
    해당 변수를 render함수를 이용, post_detail.html템플릿을 이용해 리턴 (post변수는 'post'키로 전달되도록 한다)
    """
    print('post_detail, pk:%s' % pk)
    # 아래와 같이 쓸 경우, pk값에 해당하는 Post객체가 존재하지 않을 경우
    # DoesNotExist에러 발생
    # post = Post.objects.get(pk=pk)

    # Post객체가 존재하지 않을 경우에는 404Error를 리턴해준다
    post = get_object_or_404(Post, pk=pk)

    # Post의 Comment목록 쿼리
    # comments = Comment.objects.filter(post=post)

    # ForeignKey관계에서의 역참조
    comments = post.comment_set.order_by('-created_date')

    print('post_detail, post:%s' % post)
    context = {
        'post': post,
        'comments': comments,
    }
    print('post_detail, context:%s' % context)
    return render(request, 'blog/post_detail.html', context)


from .forms import PostForm
from django.http import HttpResponse
from django.shortcuts import redirect
def post_new(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse('로그인하세요!')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # 앞의 blog는 mysite/urls.py의 include('blog.urls')의 namespace
            return redirect('blog:post_detail', pk=post.pk)

        # 테스트용
        # data_form_is_valid = form.is_valid()
        # data_title = request.POST['title']
        # data_text = request.POST['text']
        # data_str = '%s : %s (유효검사:%s)' % (
        #     data_title,
        #     data_text,
        #     data_form_is_valid
        # )
        # return HttpResponse(data_str)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(data=request.POST, instance=post)
        # form2 = PostForm(data=request.POST)
        # form3 = PostForm(instance=post)
        # print(form.data)
        # print(form2.data)
        # print(form3.data)
        # print(form.is_valid())
        # print(form2.is_valid())
        # print(form3.is_valid())
        # print(form3.initial)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


def comment_add(request, post_pk):
    """
    기능을 새로 만들고싶다
    1. 해당 기능의 처리결과를 저장할 수 있는 데이터베이스 model 생성
    2. 기능을 처리하는 view구현
    3. 해당 view에 요청을 하기위한 urls.py설정
    4. view의 기능을 보여주는 template구현

    1. Comment model생성
    2. db migration
    3. post_detail.html에 form추가 (직접!) -> comment_add쪽으로 POST요청하는 form생성
    4. comment_add view생성 및 url과 연결 (pk값을 받아서 어떤 Post인스턴스에 Comment를 생성하는지 구분)
    5. comment_add view에서 POST요청 받아서 Comment 인스턴스 생성
    6. post_detail view로 redirect
    """
    if request.method == 'POST':
        from blog.models import Comment
        # Comment를 추가할 Post인스턴스 파악
        post = Post.objects.get(pk=post_pk)

        # POST요청에서 'content'라는 키값으로 전달된 내용을 content변수에 할당
        content = request.POST['content']

        # 위에서 정의한 Post인스턴스와 내용(content)로
        # post.comment_set.create(
        #     content=content
        # )
        comment = Comment.objects.create(
            post=post,
            content=content
        )
        messages.success(request, '댓글을 달았습니다!')
        return redirect('blog:post_detail', pk=post.pk)

# Django girls

튜토리얼 진행해주세요

-

# 로그인/로그아웃 구현

[Using the Django authentication system - Auth web requests](https://docs.djangoproject.com/en/1.10/topics/auth/default/#auth-web-requests)  

**authenticate**  
username, password를 받아 인증에 성공할 경우 User객체를 리턴 (실패시 None리턴)

**login**  
request, user를 받아 해당 user를 전달받은 request환경에서 로그인이 유지되도록 함

-

### View 작성

```python
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import \
    authenticate as auth_authenticate, \
    login as auth_login
# https://docs.djangoproject.com/en/1.10/
# topics/auth/default/#auth-web-requests


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth_authenticate(
        username=username,
        password=password
    )

    if user is not None:
        auth_login(request, user)
        return HttpResponse('로그인 되었습니다')
    else:
        return HttpResponse('로그인에 실패하였습니다')
        
        
```

### urls.py작성 및 프로젝트 urls.py와 연결

`member/urls.py`

```python
from django.conf.urls import url
from .views import login

urlpatterns = [
    url(r'^login/$', login, name='login'),
]
```

`mysite/urls.py`

```python
url(r'^member/', include('member.urls', namespace='member')),
```


from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import login as auth_login

__all__ = [
    'login',
    'login_facebook',
]


def login(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            return HttpResponse('username 또는 password는 필수항목입니다')
        user = auth_authenticate(
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            messages.success(request, '로그인에 성공하였습니다')
            return redirect(next)
        else:
            messages.error(request, '로그인에 실패하였습니다')
            return render(request, 'member/login.html', {})
    else:
        return render(request, 'member/login.html', {})


def login_facebook(request):
    if request.GET.get('error'):
        messages.error(request, '사용자가 페이스북 로그인을 취소했습니다')
        return redirect('member:login')

    if request.GET.get('code'):
        from django.conf import settings
        import requests
        import json
        APP_ID = settings.FACEBOOK_APP_ID
        SECRET_CODE = settings.FACEBOOK_SECRET_CODE
        APP_ACCESS_TOKEN = '{app_id}|{secret_code}'.format(
            app_id=APP_ID,
            secret_code=SECRET_CODE
        )
        REDIRECT_URL = 'http://127.0.0.1:8000/member/login/facebook/'

        # 사용자가 페이스북로그인 버튼을 눌러 페이스북에서 로그인에 성공했을 경우,
        # 페이스북에서 mysite로 access_token을 요청할 수 있는 'code'값을 보내준다
        code = request.GET.get('code')
        print('code : %s' % code)

        # 받은 'code'값과 client_id, client_secret값을 사용해서 access_token을 얻는다
        url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token?' \
                                   'client_id={client_id}&' \
                                   'redirect_uri={redirect_uri}&' \
                                   'client_secret={client_secret}&' \
                                   'code={code}'.format(
                                        client_id=APP_ID,
                                        redirect_uri=REDIRECT_URL,
                                        client_secret=SECRET_CODE,
                                        code=code
                                    )
        r = requests.get(url_request_access_token)
        dict_access_token = r.json()
        # print(json.dumps(dict_access_token, indent=2))
        ACCESS_TOKEN = dict_access_token['access_token']
        print('ACCESS_TOKEN : %s' % ACCESS_TOKEN)

        # 얻어낸 'access_token'의 유효성을 검사하며, 또한 user_id값을 얻어낸다
        # 이때, input_token에는 위에서 얻은 'access_token'을 사용하며,
        # access_token에는 {app_id}|{secret_code} 형태의 APP_ACCESS_TOKEN을 사용한다
        url_debug_token = 'https://graph.facebook.com/debug_token?' \
                          'input_token={it}&' \
                          'access_token={at}'.format(
                                it=ACCESS_TOKEN,
                                at=APP_ACCESS_TOKEN
                            )
        r = requests.get(url_debug_token)
        dict_debug = r.json()
        print(json.dumps(dict_debug, indent=2))
        USER_ID = dict_debug['data']['user_id']
        print('USER_ID : %s' % USER_ID)

        # debug에서 받아온 USER_ID를 이용해서 graph API에 유저 정보를 요청
        url_request_user_info = 'https://graph.facebook.com/' \
                                '{user_id}?' \
                                'fields=id,first_name,last_name,gender,picture,email&' \
                                'access_token={access_token}'.format(
                                    user_id=USER_ID,
                                    access_token=ACCESS_TOKEN
                                )
        r = requests.get(url_request_user_info)
        dict_user_info = r.json()
        print(json.dumps(dict_user_info, indent=2))

        # authenticate backends에 FacebookBackend추가해서 dict_user_info객체로 로그인 가능
        user = auth_authenticate(user_info=dict_user_info)
        if user is not None:
            auth_login(request, user)
            messages.success(request, '페이스북 유저로 로그인 되었습니다')
            return redirect('blog:post_list')
        else:
            messages.error(request, '페이스북 로그인에 실패하였습니다')
            return redirect('member:login')


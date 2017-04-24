from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import \
    authenticate as auth_authenticate, \
    login as auth_login, \
    logout as auth_logout

# https://docs.djangoproject.com/en/1.10/
# topics/auth/default/#auth-web-requests


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


def logout(request):
    auth_logout(request)
    messages.info(request, '로그아웃 되었습니다')
    return redirect('blog:post_list')



# def signUp(request):
#     # from IPython import embed; embed()
#     if not request.method == 'POST':
#         return render(request, 'dgirls/signup.html')
#     else :
#         userid = request.POST['userid']
#         passwd = request.POST['passwd']
#         email = request.POST['email']
#
#         if User.objects.get(userid=userid).exsits():
#             return redirect("dgirls:signup", {'msg': '존재하는 ID'})
#         else :
#             s = sha512()
#             s.update(SALT)
#             s.update(passwd.encode("ascii"))
#             user = User.objects.create(userid=userid, passwd=passwd, email=email)
#
#             auth_login(reqeust, user)
#
#             return render(request, 'dgirls/index.html')

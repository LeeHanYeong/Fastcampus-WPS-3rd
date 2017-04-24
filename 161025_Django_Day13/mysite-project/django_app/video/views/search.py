from django.shortcuts import render
from video.apis.youtube import youtube_search

# 이 모듈을 import시킬 때
# from views.search import *
# 을 입력해도 search함수만 import하게된다
__all__ = ['search']


def search(request):
    # Template : 'video/search.html'
    # URL : 'video/search/'
    # view : search
    # Static, Templates 디렉토리 설정
    """
    1. STATICFILES_DIRS 설정
    2. templates폴더 생성 후 TEMPLATE의 DIRS안에 설정
    3. video/search.html파일 생성
    4. search.html내부 내용
        input
        ul > li (img, p*3)
    5. urls.py에 view연결
    6. view에서 video/search.html파일 render
    """
    # GET paramter에서 keyword값을 가져옵니다

    # 빈 dict요소 생성
    context = {}

    # request.GET의 parameter에서 keyword, page_token값을 가져옴
    keyword = request.GET.get('keyword')
    page_token = request.GET.get('page_token')

    # 만약 keyword값이 존재할 경우 (request.GET의 keyword키로 값이 넘어올 경우)
    # context dict에 keyword, response에 값 할당해줌
    if keyword:
        response = youtube_search(keyword, page_token)
        context['keyword'] = keyword
        context['response'] = response
    # 검색을 안 할 경우 빈 dict요소만 가지고 렌더링
    return render(request, 'video/search.html', context)
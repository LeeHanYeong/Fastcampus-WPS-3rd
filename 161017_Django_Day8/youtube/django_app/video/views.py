from django.shortcuts import render
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = "AIzaSyDiarbwPOxSkXmNPfdv8UtHcZM6KySpk34"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(keyword, page_token, max_results=10):
    """
    youtube_search함수 개선

    1. youtube_search 함수의 arguments에 pageToken 추가
    2. 받은 pageToken값을 youtube.search()실행 시 list의 인자로 추가
    3. search뷰에서 request.GET에 pageToken값을 받아오도록 설정
    4. template에서 이전페이지/다음페이지 a태그 href에 GET parameter가 추가되도록 설정
    """
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    search_response = youtube.search().list(
        q=keyword,
        part="id,snippet",
        maxResults=max_results,
        pageToken=page_token
    ).execute()

    return search_response

import json
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


def add_bookmark(request):
    """
    POST요청을 받음

    kind
    videoId
    title
    description
    publishedAt
    thumbnails

    요소들을 사용해서​
        Video 인스턴스 생성 후
        받았던 페이지로 돌아가기
        request.path값을 POST안에 받아서 돌아와야 됨
    """
    pass


def bookmark_list(request):
    """
    추가한 Video인스턴스 목록을 보여주는 페이지
    """
    pass
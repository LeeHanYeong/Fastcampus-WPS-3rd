# 인스타그램 서비스 설계

인스타그램과 유사한 데이터베이스 구조를 설계하고, API를 제작해봅니다.

## DB 구조

**사용자 계정 (member.MyUser)**  

**Fields**

- username
- password
- last_name
- first_name
- img_profile
- following_users (MTM Intermediate to self, symmetric False)
- block_users (MTM Intermediate to self, symmetric False)
	- 다른 MyUser와 Follower, Following, Block관계를 가져야 함

**Method**

friends() : 해당 유저와 서로 following한 user의 목록 리턴  
follow(user) : 해당 유저를 following하도록 함  
unfollow(user) : 해당 유저로의 following을 해제  
block(user): 해당 유저를 block하도록 함  
unblock(user): 해당 유저의 block을 해제한다  

	
**사진 (photo.Photo)**

- image (포스트 1개의 이미지파일)
- author (올린사람)
- content (포스트의 내용)
- tags (MTM PhotoTag) (태그 목록)
- like_users (MTM, intermediate model PhotoLike)

**사진 태그 (photo.PhotoTag)**

> 해시태그 형태로 동작

- title (태그명)


**사진 댓글 (photo.PhotoComment)**

- photo (해당 Photo)
- author (작성자)
- content (댓글내용)


**사진 좋아요 (photo.PhotoLike)**

- photo (해당 사진)
- user (좋아요 누른 유저)
- created_date (자동)


## API

**API**  
> https://ko.wikipedia.org/wiki/API

어떠한 기능을 사용할 수 있도록 호출할 수 있게 정의된 형태


**RESTful**
> https://ko.wikipedia.org/wiki/REST

URL(URI)형태만으로 이 API가 어떤 동작을 하는지 유추할 수 있도록 하는 구조



## API List

- Photo List
- Photo add
- Comment add


## Photo List View

1. MEDIA_URL을 settings.py에 등록
2. 메인 urls.py에 static 함수 이용해서 MEDIA_ROOT의 경로를 참조하도록 추가
3. photo앱의 views.py에 photo_list(request) 뷰 작성
4. photo앱의 urls모듈에 views.py작성
4. photo앱의 urls의 views.py에 photo_list를 연결
5. 메인 urls.py에 photo앱의 urls.views모듈을 include로 연결
6. templates폴더 생성, settings.py에서 TEMPLATE_DIRS에 해당 경로 등록
7. photo_list뷰를 보여주는 template파일 작성
8. 완성!


## JavaScript 결제 라이브러리

<http://iamport.kr/>


## DRF 한글 번역

<http://raccoonyy.github.io/drf3-tutorial-1/>
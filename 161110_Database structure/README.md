# 인스타그램 서비스 설계

인스타그램과 유사한 데이터베이스 구조를 설계하고, API를 제작해봅니다.

## DB 구조

**사용자 계정 (member.MyUser)**  

- username
- password
- last_name
- first_name
- img_profile
- like_photos
	- PhotoLike목록
- follower, following, block (MTM Intermediate to self, symmetric False)
	- 다른 MyUser와 Follower, Following, Block관계를 가져야 함
	
**사진 (photo.Photo)**

- image
- author
- content
- tags (MTM PhotoTag)

**사진 태그 (photo.PhotoTag)**

> 해시태그 형태로 동작

- title


**사진 댓글 (photo.PhotoComment)**

- author
- content


**사진 좋아요 (photo.PhotoLike)**

- photo
- user
- created_date


## API

설계해봅시다
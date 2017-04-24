# Email

[Django Email](https://docs.djangoproject.com/en/1.10/topics/email/)

-

# SMS API

[coolsms](http://www.coolsms.co.kr/)  
[Python SDK사용법](http://www.coolsms.co.kr/Python_SDK_Start_here)  


-

# 서버 세팅

### 연결 구조

- 도메인에 Cloudflare의 네임서버 사용
- Cloudflare의 DNS세팅에 접속할 IP세팅

-


#### 네임서버  

http://lhy.kr과 같은 도메인을 238.128.013.223과 같은 IP주소로 매핑시켜주는 서버  
네임서버를 관리하는 서버가 최상위 레벨이어야 변경시 적용이 빠름

#### A레코드와 CNAME의 차이

- A레코드
	- IP주소를 통해 직접 연결
- C레코드
	- 도메인으로 연결 후 해당 도메인의 IP주소를 다시 찾음

-

#### CDN

**Content Distribution Network**  
대용량 파일들을 분산된 서버로 운영하여, 요청에서 가까운 지역의 서버에서 전송해주는 서비스

-


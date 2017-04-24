# 추가사항

### Token Authentication 사용시 EB 세팅

> 근택님이 제보해주셨습니다  
> 매우감사합니당  
> 밥 사드리겠습니당(굽신)

config파일에 아래 내용을 적어줍니다.  
Apache에서는 기본적으로 Session인증만을 지원하기 때문에, 아래 문구를 사용해서 세션 이외의 인증을 허용해야 합니다.

```
container_commands:
  01_wsgipass:
    command: 'echo "WSGIPassAuthorization On" >> ../wsgi.conf'
```

-


### DRF에서 DateTimeField localtime으로 보내기

<http://stackoverflow.com/questions/34275588/djangorestframework-modelserializer-datetimefield-only-converting-to-current-tim>

-


### RDS (PostgreSQL) Database삭제 후 Create

**삭제시**

```
psql -h <DB host> -p 5432 -U <DB username> -d postgres -c "DROP DATABASE \"<DB name>\";"
```

**생성시**

```
psql -h <DB host> -p 5432 -U <DB username> -d postgres -c "CREATE DATABASE \"<DB name>\";"
```

**ex)**  

```
psql -h fastcampus.cryfbwalveyh.ap-northeast-2.rds.amazonaws.com -p 5432 -U lhy -d postgres -c "DROP DATABASE \"fastcampus\";"
```

-


### 협업시 Fork사용

<http://dogfeet.github.io/articles/2012/how-to-github.html>

-


### CORS문제 해결

**공식문서**  
<http://www.django-rest-framework.org/topics/ajax-csrf-cors/>

**django-cors-headers**  
<https://github.com/ottoyiu/django-cors-headers/>

문서에서 `INSTALLED_APPS`, `MIDDLEWARE`, `CORS_ORIGIN_WHITELIST` 세부분만 설정해주시면 됩니다.


-


### AWS Monitoring

<http://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/customize-containers-cw.html>  
<http://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/environments-health.html>


# Elasticbeanstalk 복습

> eb deploy전에는 git commit하셔야 합니다.

### Django 프로젝트 폴더 생성

**전체 프로젝트 폴더**  
eb-again-project/

**Django 프로젝트 폴더**  
eb-again-project/django_app/

**Django 프로젝트 이름**  
eb_again

**구조**  

- eb-again-project/
	- .git/
	- .gitignore
	- .python-version
	- requirements.txt
	- .ebextensions/
	- .elasticbeanstalk/
	- django_app/
		- manage.py
		- eb_again/
			- settings.py
			- urls.py
			- wsgi.py

### AWS IAM User생성

IAM -> Users -> Create New Users -> fastcampus -> credentials.cvs 다운로드

### EB 및 env 생성

```
eb init
eb create
```

### WSGI path 지정하는 설정파일 생성

```
mkdir .ebextensions
vi .ebextensions/django.config

option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: django_app/eb_again/wsgi.py
    NumProcesses: 3
    NumThreads: 20
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: eb_again.settings
    PYTHONPATH: /opt/python/current/app/django_app:$PYTHONPATH
    LANG: "ko_KR.utf8"
    LC_ALL: "ko_KR.UTF-8"
    LC_LANG: "ko_KR.UTF-8"
```

### Commit후 deploy

```
git add -A
git commit
eb deploy
```

### Elasticbeanstalk - RDS 연결 공식문서

<http://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/AWSHowTo.RDS.html>







# AWS RDS, S3 연결

## AWS RDS 연결

> <http://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/create-deploy-python-rds.html>

#### PostgreSQL RDS생성



#### 배포용 settings_deploy.json파일 생성

```
mkdir .django-conf
cd .django-conf
vi settings_deploy.json

{
  "databases": {
    "default": {
      "ENGINE": "django.db.backends.postgresql_psycopg2",
      "NAME": "<db name>",
      "USER": "<db user>",
      "PASSWORD": "<db password>",
      "HOST": "<db endpoint>",
      "PORT": "5432"
    }
  }
}
```

#### 설정 폴더들은 .gitignore에 추가

```
vi .gitignore

.aws-conf/
.django-conf/
```

#### settings.py에 DEBUG판단 구문 추가

```python
DEBUG = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')
```

#### DIRS추가

```
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
CONF_DIR = os.path.join(ROOT_DIR, '.django-conf')
STATIC_ROOT = os.path.join(ROOT_DIR, 'static_root')
```

### static_root폴더는 .gitignore에 추가

```
vi .gitignore
static_root/
```

#### DEBUG 여부에 따라 config 다르게 불러오기

```python
if DEBUG:
    config = json.loads(open(os.path.join(CONF_DIR, 'settings_debug.json')).read())
else:
    config = json.loads(open(os.path.join(CONF_DIR, 'settings_deploy.json')).read())
```

#### settings.py의 DATABASES세팅 정의

```python
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = config['databases']
```

#### psycopg2 패키지 설치

```
pip install psycopg2
```

#### 서버에서 psycopg2 패키지 실행을 위해 yum패키지 관리자에서 postgresql95-devel을 설치하도록 함

`.ebextensions/packages.config`

```
packages:
  yum:
    postgresql95-devel: []
```

#### .ebignore파일을 이용해 configuration json파일은 eb deploy시 업로드 되도록 함

`vi .ebignore`

```
!.django-conf/
```

#### /static/에서 찾을 경로 지정

`django.config`

```
aws:elasticbeanstalk:container:python:staticfiles:
    "/static/": "static_root/"
```

#### .ebextensions/django.config에 배포시 실행할 커맨드 추가

```
container_commands:
  01_collectstatic:
    command: "source /opt/python/run/venv/bin/activate && python django_app/manage.py collectstatic --noinput"
  02_migrate:
    command: "source /opt/python/run/venv/bin/activate && python django_app/manage.py migrate --noinput"
```

#### DB connection 에러 날 시

EC2 Security Group의 SecurityGroup for ElasticBeanstalk environment인 GroupID를 RDS의 SecurityGroup의 Inbound에 추가해준다.

RDS SecurityGroup선택 -> Edit -> Add Rule -> PostgreSQL -> Source에 추가할 GroupID로 자동완성되는지 확인 후 추가 -> Save

#### superuser로 사용될 user/password를 settings_deploy.json에 추가

```
"defaultSuperuser": {
	"username": "<username>",
	"password": "<password>"
}
```

#### member app추가, management모듈 추가

settings.py의 INSTALLED_APPS에 추가

```
python manage.py startapp member
```

`member/management/commands/createsu.py`

```
import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
User = get_user_model()
CONF_DIR = settings.CONF_DIR
config = json.loads(open(os.path.join(CONF_DIR, 'settings_deploy.json')).read())


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = config['defaultSuperuser']['username']
        password = config['defaultSuperuser']['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email='a@a.com',
                password=password
            )
        else:
            print('default superuser exist')

```

#### django.config의 container_commands에 deploy시마다 createsu command를 실행하도록 설정

`django.config`

```
03_createsu:
    command: "source /opt/python/run/venv/bin/activate && python django_app/manage.py createsu"
    leader_only: true
```



## S3 Bucket 생성 및 연결

> <https://realpython.com/blog/python/deploying-a-django-app-to-aws-elastic-beanstalk/>  
> 
> **AWS CLI**  
> <http://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-chap-getting-started.html>
> 
> **Boto**  
> AWS SDK for Python  
> <http://boto.cloudhackers.com/en/latest/index.html>
> 
> **django-storages**  
> django-storages is a collection of custom storage backends for Django.  
> <http://django-storages.readthedocs.io/en/latest/>



```
pip install awscli boto django-storages
```

#### AWS CLI 기본설정

> 설정 내용은 ~/.aws/config, credentials에서 확인가능

```
aws configure

AWS Access Key ID [None]: 
AWS Secret Access Key [None]: 
Default region name [None]: ap-northeast-2
Default output format [None]: json
```

#### IAM User가 S3사용권한을 갖도록 설정

AmazonS3FullAccess Policy를 추가

#### boto를 이용해 bucket생성

```
python
import boto
conn = boto.connect_s3('accesskey', 'secretkey')
conn.create_bucket('사용할 bucket이름')
```

#### IAM User의 ARN을 확인

IAM -> Users -> 해당유저 선택 -> Summary -> User ARN확인  
arn:aws:iam::<유저구분문자>

#### S3 Bucket의 Properties의 Permissions에 bucket policy추가

S3 -> Bucket선택 -> 우측위 Properties탭 클릭 -> Permissions클릭 -> Add bucket policy 클릭

```
BUCKET-NAME과 USER-ARN부분을 채워줌
{
    "Statement": [
        {
          "Sid":"PublicReadForGetBucketObjects",
          "Effect":"Allow",
          "Principal": {
                "AWS": "*"
             },
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::BUCKET-NAME/*"
          ]
        },
        {
            "Action": "s3:*",
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::BUCKET-NAME",
                "arn:aws:s3:::BUCKET-NAME/*"
            ],
            "Principal": {
                "AWS": [
                    "USER-ARN"
                ]
            }
        }
    ]
}
```

#### Storage Backend작성

`eb-mysite-project/django_app/eb_mysite/custom_storages.py`

```
from django.conf import settings
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION

```

#### settings.py에 django-storages사용하도록 INSTALLED_APPS에 추가

```
INSTALLED_APPS = [
	...
	'storages',
]
```

#### .conf/settings_deploy.json에 AWS관련 내용 추가

> json형식은 마지막 쉼표(,)를 허용하지 않으니, 문법에 어긋나지 않는지 잘 확인  
> DEBUG = True의 경우에도 사용할 수 있으니, 양 쪽 파일에 모두 적어준다

```
{
  "aws": {
    "AWS_STORAGE_BUCKET_NAME": "",
    "AWS_ACCESS_KEY_ID": "",
    "AWS_SECRET_ACCESS_KEY": ""
  }
}
```

#### settings.py에 관련 설정 추가


```
STATIC_S3 = True

if not DEBUG or STATIC_S3:
	AWS_HEADERS = {
	    'Expires': 'Thu, 31 Dec 2199 20:00:00 GMT',
	    'Cache-Control': 'max-age=94608000',
	}
	AWS_STORAGE_BUCKET_NAME = config['aws']['AWS_STORAGE_BUCKET_NAME']
	AWS_ACCESS_KEY_ID = config['aws']['AWS_ACCESS_KEY_ID']
	AWS_SECRET_ACCESS_KEY = config['aws']['AWS_SECRET_ACCESS_KEY']
	AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
	
	STATICFILES_LOCATION = 'static'
	STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
	STATICFILES_STORAGE = 'mysite.custom_storages.StaticStorage'
	
	MEDIAFILES_LOCATION = 'media'
	MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
	DEFAULT_FILE_STORAGE = 'mysite.custom_storages.MediaStorage'
else:
	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
	STATIC_URL = '/static/'
	MEDIA_URL = '/media/'
```


#### collectstatic 작동되는지 확인
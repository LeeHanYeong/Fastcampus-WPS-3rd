# Elasticbeanstalk Deploy

> PaaS - Plastform as a Service  
> <https://ko.wikipedia.org/wiki/PaaS>  
> <https://aws.amazon.com/ko/elasticbeanstalk>  

> 참조사이트  
> <https://realpython.com/blog/python/deploying-a-django-app-and-postgresql-to-aws-elastic-beanstalk/>

## 새 프로젝트 작성

> Django 프로젝트명은 eb_mysite  
> 가상환경은 eb-mysite-env


**프로젝트는 아래와 같은 구조**

- eb-mysite-project/
	- .git
	- .python-version
	- requirements.txt
	- django_app/
		- eb_mysite/
		- manage.py


```
cd <프로젝트 관리폴더>
mkdir eb-mysite-project
pyenv virtualenv 3.4.3 eb-mysite-env
pyenv local eb-mysite
pip install django
django-admin startproject eb_mysite
mv eb_mysite django_app
```

## AWS Security Credentials 생성

#### Security Credentials 생성
AWS메인 -> 사용자이름 클릭 -> Security Credentials  
-> Continue to Security Credentials -> Users -> Create New Users

fastcampus-eb 유저 생성 -> AccessKeyId, SecretAccessKey 확인 및 저장 (credentials.csv)

#### 해당 User에게 Elasticbeanstalk 관리권한 부여
<http://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/iam-instanceprofile.html>  
Permissions Tab클릭 -> Attach Policy

- AdministratorAccess
- AWSElasticBeanstalkWebTier
- AWSElasticBeanstalkWorkerTier
- AWSElasticBeanstalkMulticontainerDocker
- 그 외 2개도 체크



## AWS EB Application 생성

> <http://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/eb-cli3.html>


#### EB CLI설치

```
pip install awsebcli
```

#### EB init

```
eb init
Select a default region
1) us-east-1 : US East (N. Virginia)
2) us-west-1 : US West (N. California)
3) us-west-2 : US West (Oregon)
4) eu-west-1 : EU (Ireland)
5) eu-central-1 : EU (Frankfurt)
6) ap-south-1 : Asia Pacific (Mumbai)
7) ap-southeast-1 : Asia Pacific (Singapore)
8) ap-southeast-2 : Asia Pacific (Sydney)
9) ap-northeast-1 : Asia Pacific (Tokyo)
10) ap-northeast-2 : Asia Pacific (Seoul)
11) sa-east-1 : South America (Sao Paulo)
12) cn-north-1 : China (Beijing)
13) us-east-2 : US East (Ohio)
(default is 3): 10 <Enter>

You have not yet set up your credentials or your credentials are incorrect 
You must provide your credentials.
(aws-access-id): <access id>
(aws-secret-key): <secret key>

Enter Application Name
(default is "eb-mysite-project"): eb-mysite

Application eb-mysite has been created.

Select a platform.
1) Ruby
2) Go
3) Java
4) Tomcat
5) PHP
6) Python
7) Node.js
8) IIS
9) Docker
10) GlassFish
(default is 1): 6

Select a platform version.
1) Python 3.4
2) Python
3) Python 2.7
4) Python 3.4 (Preconfigured - Docker)
(default is 1): 1
Do you want to set up SSH for your instances?
(y/n): y

Select a keypair.
1) fastcampus
2) [ Create new KeyPair ]
(default is 2): 1
```

#### Elasticbeanstalk application 생성 확인

<https://ap-northeast-2.console.aws.amazon.com/elasticbeanstalk/home?region=ap-northeast-2#/applications>


## AWS EB environment 생성

> Load Balancing 옵션  
> <https://aws.amazon.com/ko/elasticloadbalancing/>  
> <http://blog.msalt.net/76>

#### Environment 생성

```
eb create
```

#### 설정파일 작성

```
mkdir .ebextensions
vi django.config

option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: django_app/eb_mysite/wsgi.py
    NumProcesses: 3
    NumThreads: 20
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: eb_mysite.settings
    PYTHONPATH: /opt/python/current/app/django_app:$PYTHONPATH
    LANG: "ko_KR.utf8"
    LC_ALL: "ko_KR.UTF-8"
    LC_LANG: "ko_KR.UTF-8"
```

#### 변경사항 배포

```
eb deploy
```

#### 완료 후 사이트 열기

```
eb open
```

#### 로그 확인

```
eb logs
```
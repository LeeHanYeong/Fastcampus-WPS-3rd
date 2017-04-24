# django-sass-processor

> <https://github.com/jrief/django-sass-processor>


# django-compressor

> <https://github.com/django-compressor/django-compressor>

# django-libsass

> <https://github.com/torchbox/django-libsass>

# Celery

> <http://www.celeryproject.org>

메시지 전달을 기반으로 하는 비동기 작업 대기열 (Queue).

## Worker

Celery에서 작업을 처리하는 프로세스. 워커에 직접 작업을 추가할 수는 없고, 작업을 전달 해 줄 메세지 브로커(Message broker)가 필요.  
메세지 브로커는 여러가지가 있지만, 공식문서에서는 RabbitMQ를 가장 추천.

## Broker

메세지를 쌓아놓고 일할 수 있는 Worker가 존재할 경우, 메세지를 하나씩 전달해주는 역할


## RabbitMQ 설치

### macOS

> <https://www.rabbitmq.com/install-standalone-mac.html>

### Ubuntu

> <https://www.rabbitmq.com/install-debian.html>



## Celery 설치 및 설정

```
pip install celery
```

> <http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django>

## Celery Task 작성

```
from celery import shared_task

@shared_task
def send_mail(...)
	...
```

## Django View 작성

```
send_email.delay(...)
```

> delay를 붙이지 않으면 일반 함수로 실행

## Celery Worker 프로세스 구동

`django`루트 디렉토리에서 아래 명령어 실행

```
celery worker -A <django_project_name>
```

## Celery Flower를 통한 모니터링

작업 성공여부 모니터링

```
pip install flower
```

`django`루트 디렉토리에서 아래 명령어 실행

```
flower -A <django_project_name>
```

`localhost:5555`로 접속해서 확인

## Daemonization

> <http://docs.celeryproject.org/en/latest/userguide/daemonizing.html#daemonizing>



# Cache

> <https://docs.djangoproject.com/en/1.10/topics/cache/>

**Ubuntu**  

```
sudo apt-get install memcached

sudo apt-get install -y \
libmemcached-dev zlib1g-dev libssl-dev python-dev build-essential
```

```
프로세스 돌고있는지 확인
ps -ax | grep memcached
```


# Crontab (리눅스 반복 예약작업)

> <http://zetawiki.com/wiki/%EB%A6%AC%EB%88%85%EC%8A%A4_%EB%B0%98%EB%B3%B5_%EC%98%88%EC%95%BD%EC%9E%91%EC%97%85_cron,_crond,_crontab>


## EB에서 사용


```
<anyname>.config

container_commands:
  01_remove_old_cron_jobs:
    command: "crontab -r || exit 0"
  02_cronjobs:
    command: "cat .ebextensions/cron.txt | crontab"
    leader_only: true
```

> cron.txt파일 마지막줄에 newline이 있어야합니다.


# API Documentation

> <https://iazelf.gitbooks.io/instagram-project-api-documentation/content/>
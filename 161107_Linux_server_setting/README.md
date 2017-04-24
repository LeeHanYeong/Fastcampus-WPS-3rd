# Ubuntu Linux Deploy

> AWS EC2 + Ubuntu16.04 + Nginx + uWSGI + Django

## 개념

**Ubuntu Linux**  
서버의 OS

**Nginx**  
웹 서버. 클라이언트로부터의 HTTP요청을 받아 정적인 페이지/파일을 돌려준다.

**Django**  
웹 애플리케이션. 웹 요청에 대해 동적데이터를 돌려준다.

**uWSGI**  
웹 서버(Nginx)와 웹 애플리케이션(Django)간의 연결을 중계해준다.  
(Nginx에서 받은 요청을 Django에서 처리하기 위한 중계인 역할을 해준다)  

**WSGI**  
Web Server Gateway Interface  
파이썬에서 웹 서버와 웹 애플리케이션간의 동작을 중계해주는 인터페이스  
[Wikipedia](https://ko.wikipedia.org/wiki/%EC%9B%B9_%EC%84%9C%EB%B2%84_%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4_%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4)

## Instance생성

#### Key Pairs생성

다운받은 .pem파일을 ~/.ssh폴더에 넣기

#### UNPROTECTED PRIVATE KEY FILE에러

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '/Users/Arcanelux/.ssh/fastcampus.pem' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "/Users/Arcanelux/.ssh/fastcampus.pem": bad permissions
Permission denied (publickey).
```

위와같은 경우, chmod 400 <pem file>로 소유주만 읽을 수 있도록 권한설정을 해준다.


#### 언어팩 설치

```
sudo apt-get install language-pack-ko
sudo locale-gen ko_KR.UTF-8
```

## Ubuntu 기본 설정

#### python-pip설치

```
sudo apt-get install python-pip
```

#### zsh 설치

```
sudo apt-get install zsh
```


#### oh-my-zsh 설치

```
sudo curl -L http://install.ohmyz.sh | sh
```


#### Default shell 변경

```
sudo chsh ubuntu -s /usr/bin/zsh
```

#### pyenv requirements설치

[공식문서](https://github.com/yyuu/pyenv/wiki/Common-build-problems)

```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils
```

#### pyenv 설치

```
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

#### pyenv 설정 .zshrc에 기록

```
vi ~/.zshrc
export PATH="/home/ubuntu/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```


#### Pillow 라이브러리 설치

[공식문서](https://pillow.readthedocs.io/en/3.4.x/installation.html#basic-installation)

```
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```



## Django 관련 설정

#### 장고 애플리케이션은 /srv Directory 사용

```
sudo chown -R ubuntu:ubuntu /srv/
```

[관련설명]  
<http://www.thegeekstuff.com/2010/09/linux-file-system-structure/?utm_source=tuicool>

#### 프로젝트 Clone

```
git clone <자신의 프로젝트>
```

#### pyenv 3.4.3설치 및 virtualenv생성

```
cd <clone한 폴더>
pyenv install 3.4.3
pyenv virtualenv mysite
pyenv local mysite
```

#### requirements설치

```
pip install -r requirements.txt
```

#### runserver 테스트

```
cd mystie
./manage.py runserver 0:8080
```

#### AWS Secutiriy Groups 8080 Port추가

Security Groups -> Inbound -> Edit -> Custom TCP Rule -> 8080

#### ALLOWED_HOSTS 설정

```
vi mysite/settings.py
ALLOWED_HOSTS = [
	'<ec2 domain name'>,
	또는
	'.amazonaws.com',
]
```


## uWSGI 관련 설정

#### 웹 서버 관리용 유저 생성

```
sudo adduser nginx
```

#### uWSGI설치

```
(virtualenv 환경 내부에서)
pip install uwsgi
```

#### uWSGI 정상 동작 확인

```
uwsgi --http :8080 --home (virtualenv경로) --chdir (django프로젝트 경로) -w (프로젝트명).wsgi
```

ex) pyenv virtualenv이름이 mysite-env, django프로젝트가 /srv/mysite/django_app, 프로젝트명이 mysite일 경우

```
uwsgi --http :8080 --home ~/.pyenv/versions/mysite-env --chdir /srv/mysite/django_app -w mysite.wsgi
```

실행 후 <ec2도메인>:8080으로 접속하여 요청을 잘 받는지 확인

#### uWSGI 사이트 파일 작성

```
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/sites
sudo vi /etc/uwsgi/sites/mysite.ini

[uwsgi]
chdir = /srv/mysite/django_app # Django application folder
module = mysite.wsgi:application # Django project name.wsgi
home = /home/ubuntu/.pyenv/versions/mysite # VirtualEnv location

uid = nginx
gid = nginx

socket = /tmp/mysite.sock
chmod-socket = 666
chown-socket = nginx:nginx

enable-threads = true
master = true
pidfile = /tmp/mysite.pid
```

#### uWSGI site파일로 정상 동작 확인

```
uwsgi --http :8080 -i /etc/uwsgi/sites/mysite.ini
```

sudo로 root권한으로 실행

```
sudo /home/ubuntu/.pyenv/versions/mysite/bin/uwsgi --http :8080 -i /etc/uwsgi/sites/mysite.ini
```

#### uWSGI 서비스 설정파일 작성

```
sudo vi /etc/systemd/system/uwsgi.service

[Unit]
Description=uWSGI Emperor service
After=syslog.target

[Service]
ExecPre=/bin/sh -c 'mkdir -p /run/uwsgi; chown nginx:nginx /run/uwsgi'
ExecStart=/home/ubuntu/.pyenv/versions/mysite/bin/uwsgi --uid nginx --gid nginx --master --emperor /etc/uwsgi/sites

Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```


## Nginx 관련 설정

#### Nginx 안정화 최신버전 사전세팅 및 설치

```
sudo apt-get install software-properties-common python-software-properties
sudo add-apt-repository ppa:nginx/stable
sudo apt-get update
sudo apt-get install nginx
nginx -v
```

#### Nginx 동작 User 변경

```
sudo vi /etc/nginx/nginx.conf

user nginx;
```

#### Nginx 가상서버 설정 파일 작성

```
sudo vi /etc/nginx/sites-available/mysite

server {
    listen 80;
    server_name localhost;
    charset utf-8;
    client_max_body_size 128M;


    location / {
        uwsgi_pass    unix:///tmp/mysite.sock;
        include       uwsgi_params;
    }
}
```

#### 설정파일 심볼릭 링크 생성

```
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/mysite
```

#### sites-enabled의 default파일 삭제

```
sudo rm /etc/nginx/sites-enabled/default
```

> nginx.conf파일에 어떤 폴더에 있는 설정을 가져와서 실행할 지 적혀있음


#### uWSGI, Nginx재시작

```
sudo systemctl restart uwsgi nginx
```

-

### 오류 발생 시

#### systemctl restart시 오류 발생 시

```
(오류 발생한 서비스에 따라 아래 명령어 실행)
sudo systemctl status uwsgi.service
sudo systemctl status nginx.service
```

#### 502 Bad Gateway

**Nginx log파일 확인**  
```
cat /var/log/nginx/error.log
```

#### Nginx log파일에서 sock파일 접근 불가시

**socket파일 권한 소유자 확인**

```
cd /tmp
ls -al
-rw-r--r--  1 nginx  nginx     6 Nov  8 06:58 mysite.pid
srw-rw-rw-  1 nginx  nginx     0 Nov  8 06:58 mysite.sock

nginx가 소유자가 아닐 경우, 
sudo rm mysite.pid mysite.sock으로 삭제 후 서비스 재시작
```

-

#### AWS Secutiriy Groups 80 Port추가

Security Groups -> Inbound -> Edit -> HTTP


## Cloudflare

#### ALLOWED_HOSTS 추가



## SSL

> [Nginx에 SSL적용](https://haandol.wordpress.com/2014/03/12/nginx-ssl-%EC%A0%81%EC%9A%A9%ED%95%98%EA%B8%B0startssl-com%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC/)  
> [Cloudflare에 Custom SSL적용](https://support.cloudflare.com/hc/en-us/articles/200170466-How-do-I-upload-a-custom-SSL-certificate-Business-or-Enterprise-only-)
"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# post 애플리케이션의 views모델에서 post_list함수를 가져옵니다
from post.views import post_list

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # post/list/로 시작하는 주소에는 post_list뷰를 이용해 response를 돌려준다
    url(r'^post/list/', post_list),
]

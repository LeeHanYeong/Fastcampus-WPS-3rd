from django.conf.urls import url
from . import views

# {} <- 이거 아닙니다
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
]
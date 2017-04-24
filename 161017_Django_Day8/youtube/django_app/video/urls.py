from django.conf.urls import url
from video import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
]

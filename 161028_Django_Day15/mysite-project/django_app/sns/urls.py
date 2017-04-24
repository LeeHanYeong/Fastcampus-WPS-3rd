from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^facebook/friends_ranking/$', views.friends_ranking, name='friends_ranking'),
]

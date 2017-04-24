from django.conf.urls import url
from .. import views

urlpatterns = [
    # url(r'^login/$', views.login_fbv, name='login'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
]

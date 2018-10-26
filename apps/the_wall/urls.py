from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^wall/$', views.index),
    url(r'^users/create/$', views.user_create),
    url(r'^users/login/$', views.validate_login),
    url(r'^users/login/success/$', views.success),
    url(r'^wall/users/logout/$', views.logout),
    url(r'^wall/posts/messages/create/$', views.create_message),
    url(r'^wall/posts/(?P<number>\d+)/comments/create/$', views.create_comment),
    url(r'^wall/posts/(?P<number>\d+)/comments/delete/$', views.destroy_comment),
]


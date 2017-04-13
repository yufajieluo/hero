from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^user/$', views.user, name = 'user'),
    url(r'^user/register/$', views.register, name = 'register'),
    url(r'^user/captcha/$', views.captcha, name = 'captcha'),
    url(r'^user/welcome/$', views.welcome, name = 'welcome'),
    url(r'^user/password/$', views.password, name = 'password'),
    url(r'^user/logout/$', views.logout, name = 'logout'),
    url(r'^role/$', views.role, name = 'role'),
    url(r'^role/permission/$', views.role_permission, name = 'role_permission'),
    url(r'^permission/$', views.permission, name = 'permission'),
    url(r'^resource/$', views.resource, name = 'resource'),
    url(r'^log/$', views.log, name = 'log'),

    url(r'^restrict/article/$', views.restrict_article, name = 'restrict_article'),
    url(r'^restrict/article/content/$', views.restrict_article_content, name = 'restrict_article_content'),
    url(r'^restrict/photograph/$', views.restrict_picture, name = 'restrict_picture'),
    url(r'^restrict/photograph/content/$', views.restrict_picture_content, name = 'restrict_article_content'),
    url(r'^restrict/video/$', views.restrict_video, name = 'restrict_video'),
]

"""findu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import  views
urlpatterns = [
    url(r'^chat/', views.WeChat,name='chat'),
    url(r'^getmenu/', views.getmenu,name='getmenu'),
    url(r'^delmenu/', views.delmenu,name='delmenu'),
    url(r'^createmenu/', views.createmenu,name='createmenu'),
    url(r'^municipalhall/', views.municipalhall,name='municipalhall'),
    url(r'^wechatmatrix/', views.wechatmatrix,name='wechatmatrix'),
    url(r'^canyin/', views.canyin,name='canyin'),
    url(r'^canyindetail/', views.canyindetail,name='canyindetail'),
    url(r'^text/', views.text,name='test'),
    url(r'^charge/', views.charge,name='charge'),
]

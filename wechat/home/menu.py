# -*- coding: utf-8 -*-
'''
Created on 2017年4月13日

@author:
'''
import json
import urllib2
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.sessions.models import Session
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class MenuManager(View):
    accessUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxe840f265a71f11b8&secret=050bb9529cf251aa4d0c1f7a2565554d"
    delMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token="
    createUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token="
    getMenuUri = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token="

    def getAccessToken(self,request):
        print "access_token来了"
        if not request.session.get('access_token', False):
            print "重新获得access_token"
            f = urllib2.urlopen(self.accessUrl)
            accessT = f.read()
            jsonT = json.loads(accessT)
            request.session.set_expiry(7200)
            request.session["access_token"] = jsonT["access_token"]
        return request.session.get('access_token')
    def delMenu(self, accessToken):
        html = urllib2.urlopen(self.delMenuUrl + accessToken)
        result = json.loads(html.read())
        return result["errcode"]
    def createMenu(self, accessToken):
        menu = '''{
                 "button":[
                                 {
                      "type":"view",
                      "name":"市政大厅",
                      "url":"http://licong.iok.la:35148/home/municipalhall/"
                  },
                  {
                       "type":"view",
                       "name":"微信矩阵",
                       "url":"http://licong.iok.la:35148/home/wechatmatrix/"
                  },
                  {
                       "type":"click",
                       "name":"锡市WIFI",
                       "key" : "XM_WIFI"
                  }
                  ]
                  }'''
        req = urllib2.Request(self.createUrl + accessToken, menu)
        response = urllib2.urlopen(req)
        return response
    def getMenu(self,accessToken):
        html = urllib2.urlopen(self.getMenuUri + accessToken)
        return str(html.read())


# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.template import loader, Context
from xml.etree import ElementTree as ET
from imgtest import imgtest
import time
import hashlib
from menu import MenuManager
import json
import requests
@csrf_exempt
def WeChat(request):
  #这里我当时写成了防止跨站请求伪造，其实不是这样的，恰恰相反。因为django默认是开启了csrf防护中间件的
  #所以这里使用@csrf_exempt是单独为这个函数去掉这个防护功能。
  if request.method == "GET":

    #下面这四个参数是在接入时，微信的服务器发送过来的参数
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)

    #这个token是我们自己来定义的，并且这个要填写在开发文档中的Token的位置
    token = 'bdcloud'

    #把token，timestamp, nonce放在一个序列中，并且按字符排序
    hashlist = [token, timestamp, nonce]
    hashlist.sort()

    #将上面的序列合成一个字符串
    hashstr = ''.join([s for s in hashlist])

    #通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
    hashstr = hashlib.sha1(hashstr).hexdigest()

    #把我们生成的字符串和微信服务器发送过来的字符串比较，
    #如果相同，就把服务器发过来的echostr字符串返回去
    if hashstr == signature:
      return HttpResponse(echostr)
  if request.method == "POST":
     # print "######## wechat post method ##########"
      str_xml = request.body
      xml = ET.fromstring(str_xml)
      msgType=xml.find("MsgType").text
      toUser=xml.find("FromUserName").text
      fromUser=xml.find("ToUserName").text
      nowtime = str(int(time.time()))    
      if msgType == 'event':
           Event=xml.find("Event").text
           if Event == 'CLICK':
               EventKey=xml.find("EventKey").text
               if EventKey == 'XM_WIFI':
                  t = loader.get_template('home/tuwen.xml')
                  c = Context({'toUser': toUser, 'fromUser': fromUser,'nowtime': nowtime,
                               'title1': '锡林浩特WIFI热点分布图', 'description1':'功能开发中，敬请期待。',
                               'picurl1':'http://121.40.58.147/static/images/map-1.jpg',
                               'title2': '锡林浩特智慧旅游城市项目计划', 'description2':'功能开发中，敬请期待。',
                               'picurl2':'http://121.40.58.147/static/images/1111.jpg',
                               'title3': '智能WIFI覆盖旅游景点介绍', 'description3':'功能开发中，敬请期待。',
                               'picurl3':'http://121.40.58.147/static/images/1112.jpg',
                               'title4': '智慧锡林浩特简介', 'description4':'功能开发中，敬请期待。',
                               'picurl4':'http://121.40.58.147/static/images/1113.jpg',
                               'title5': '公共场所免费开放WIFI', 'description5':'功能开发中，敬请期待。',
                               'picurl5':'http://121.40.58.147/static/images/1114.jpg',
                               'url':'http://licong.iok.la:35148/home/text'
                               })
                  return HttpResponse(t.render(c))
           elif Event == 'subscribe':
                content = '终于等到你，感谢您的关注。'
	   else:
		content = ''
      elif msgType == 'image':
          try:
            picurl = xml.find('PicUrl').text
            datas = imgtest(picurl)
            content =  '图中人物性别为'+datas[0]+'\n'+'年龄为'+datas[1]
          except:
            content =  '识别失败，换张图片试试吧'
      else:
	  content = chat( xml.find("Content").text)
      
      #加载text.xml模板
      t = loader.get_template('home/text.xml')
      #将我们的数据组成Context用来render模板。
      c = Context({'toUser': toUser, 'fromUser': fromUser,
                   'nowtime': nowtime, 'content': content})
      #print t.render(c)
      return HttpResponse(t.render(c))
     
def createmenu(request):
    wx = MenuManager()
    accessToken = wx.getAccessToken(request)
    wx.createMenu(accessToken)
    return HttpResponse("创建成功")

def delmenu(request):
    wx = MenuManager()
    accessToken = wx.getAccessToken(request)
    wx.delMenu(accessToken)
    return HttpResponse("删除成功")

def getmenu(request):
    wx = MenuManager()
    accessToken = wx.getAccessToken(request)
    respstr = wx.getMenu(accessToken)
    print "respstr:",respstr
    return HttpResponse(respstr)

def municipalhall(request):
    return render(request,'home/municipalhall.html')

def wechatmatrix(request):
    return render(request,'home/wechatmatrix.html')

def canyin(request):
    return render(request,'home/canyin.html')

def text(request):
    return render(request,'home/text.html')

def chat(msg):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    url = 'http://www.tuling123.com/openapi/api'
    con = '''{"key":"0767b07223a94eb299c7657b9b2b5c72","info":"%s"}'''%(msg)
    print con
    response = requests.post(url,data = con.encode('utf-8'))
    print response.text
    return eval(response.text)["text"]

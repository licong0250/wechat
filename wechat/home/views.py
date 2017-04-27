# -*- coding: utf-8 -*-
from datetime import datetime
import random
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
from models import Hotel,Comment
import json
import requests
APPID = 'wxe840f265a71f11b8'
APPSECRET = '050bb9529cf251aa4d0c1f7a2565554d'

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

def getuserinfo(code):
    '''
     获得用户的昵称等信息
    :param request:
    :return:
    '''

    access_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    cont = {}
    cont["appid"] = APPID
    cont["secret"] = APPSECRET
    cont["code"] = code
    cont["grant_type"] = "authorization_code"
    cont["srtnoc"] =  random.random()

    response = requests.get(access_token_url,params=cont)

    print "response:",response.text

    retparm = eval(response.text)
    print "retparm:",retparm
    openid = retparm["openid"]
    refresh_token = retparm["refresh_token"]
    access_token = checktoken(retparm["access_token"],openid,refresh_token)
    scope = retparm["scope"]
    userparams_url = "https://api.weixin.qq.com/sns/userinfo?access_token="+access_token+"&openid="+openid+"&lang=zh_CN"
    userinfo = requests.get(userparams_url)
    userinfo.encoding = 'utf-8'
    print "用户信息：",userinfo.text
    return eval(userinfo.text)
@csrf_exempt
def canyindetail(request):
    if request.method == "GET":
        code = request.GET.get('code')
        hostid = request.GET.get('id')
        print code,"id:",id

        useinfo = getuserinfo(code)
        print "用户信息：",useinfo["nickname"]
        print "用户信息：",useinfo["headimgurl"]
        context = {}
        context["item_list"] = [1,2,3,4]
        context["nickname"] = useinfo["nickname"]
        context["useinfo"] = useinfo
        context["hostid"] = hostid
        return render(request,'home/detail.html',context)
    if request.method == "POST":
        print "I am POST "
        hostid = request.POST.get("hostid")
        useinfo = request.POST.get("useinfo")
        nickname = request.POST.get("nickname")
        point = request.POST.get("inputpoint")
        commenttext = request.POST.get("commenttext")
        images = request.FILES.getlist('commentimg')
        imagesurl = ''
        for f in images:
             url = './static/comm_images/'+ genOrderNum() + f.name
             imagesurl += url+";"
             destination = open(url,'wb+')
             for chunk in f.chunks():
                  destination.write(chunk)
             destination.close()
        print imagesurl
        print hostid,point,commenttext,images,useinfo,hostid,nickname
        context = {}
        return render(request,'home/detail.html',context)
def genOrderNum():
    _now = datetime.utcnow()
    seq = [
        '{0:04}'.format(_now.year),
        '{0:02}'.format(_now.month),
        '{0:02}'.format(_now.day),
        '{0:02}'.format(_now.hour),
        '{0:02}'.format(_now.minute),
        '{0:02}'.format(_now.second),
        '{0:06}'.format(_now.microsecond)]
    return 'COMMENT' + ''.join(seq)

def checktoken(token,openid,refresh_token):
    chekouturl = "https://api.weixin.qq.com/sns/auth?access_token="+token+"&openid="+openid
    result = requests.get(chekouturl)
    if eval(result.text)["errcode"] == 0:
        print "token有效"
        return token
    else:
        refurl = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid="+APPID+"&grant_type="+refresh_token+"&refresh_token=REFRESH_TOKEN"
        respon = requests.post(refurl)
        if eval(respon.text).has_key('access_token'):
            return eval(respon.text)["access_token"]

def canyin(request):
    hotels_info=[]
    hotels=Hotel.objects.all()
    for hotel in hotels:
        tmp_info={}
        tmp_info["posi"]=[]
        tmp_info["name"]=""
        tmp_info["id"]=None
        tmp_info["score"]=None

        tmp_info["name"]=str(hotel.name)
        tmp_info["score"]=float(hotel.avr_score)
        tmp_info["id"]=int(hotel.id)
        tmp_posi=[]
        tmp_posi.append(hotel.lng)
        tmp_posi.append(hotel.lat)
        tmp_info["posi"]=tmp_posi
        hotels_info.append(tmp_info)
    context={}
    print hotels_info,type(hotels_info)
    context["hotels_info"]=hotels_info
    return render(request,'home/canyin.html',context)

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

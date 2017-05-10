# -*- coding=utf-8 -*-

from django.db import models

class Hotel(models.Model):
    name=models.CharField(max_length=100, verbose_name='名字')
    alias=models.CharField(max_length=100,blank=True,verbose_name='别名')
    address=models.CharField(max_length=100,verbose_name='地址')
    lng=models.FloatField(verbose_name='经度')
    lat=models.FloatField(verbose_name='纬度')
    introduce=models.TextField(blank=True,verbose_name='简介')
    avr_score=models.FloatField(verbose_name='评分',default=5.0)
    img=models.CharField(max_length=2048,blank=True)
    phone = models.CharField('电话号码', max_length=100, blank=True, null=True)
    exitQnote = models.CharField('存在的问题', max_length=2048, blank=True, null=True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '餐饮店'
        verbose_name_plural = '餐饮店'



class Comment(models.Model):
    username=models.CharField(max_length=100, verbose_name='用户名')
    headimgurl=models.CharField(max_length=256, verbose_name='用户头像URL')
    comment=models.TextField(blank=True,verbose_name='评论')
    socre=models.CharField(max_length=10,verbose_name='评分',default='')
    img=models.CharField(max_length=2048,blank=True)
    hotel=models.ForeignKey(Hotel)

def updateHotelScore(hotel_id):
    item=models.Comment.objects.filter(hotel_id=hotel_id)
    pass


class ApInfo(models.Model):
    address=models.CharField("AP地址",max_length =255,blank=False, null = True)
    lng=models.FloatField("AP经度",blank=False, null = False)
    lat=models.FloatField("AP纬度",max_length=20,blank=False, null = False)
    apmac = models.CharField("AP mac地址",max_length=255,blank=False, null = False)

class Complaintext(models.Model):
    username=models.CharField(max_length=100, verbose_name='用户名')
    complaintext=models.TextField(blank=True, verbose_name='投诉内容')
    complaintime=models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    hotelid=models.IntegerField(blank=True,verbose_name='餐厅id')
    connect=models.CharField(max_length=100, verbose_name='联系方式')
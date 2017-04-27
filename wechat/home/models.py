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
    img=models.ImageField(upload_to='img',blank=True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '餐饮店'
        verbose_name_plural = '餐饮店'



class Comment(models.Model):
    comment=models.TextField(blank=True,verbose_name='评论')
    socre=models.FloatField(verbose_name='评分',default=5.0)
    img=models.ImageField(upload_to='comment_img',blank=True)
    hotel=models.ForeignKey(Hotel)

def updateHotelScore(hotel_id):
    item=models.Comment.objects.filter(hotel_id=hotel_id)
    pass
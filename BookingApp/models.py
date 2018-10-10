from django.db import models
import sqlite3

# Create your models here.
class Speech(models.Model):
    speech_name = models.TextField(verbose_name="讲座名称")
    speech_speaker_name = models.TextField(verbose_name="主讲人名称")
    speech_speaker_introduction = models.TextField(verbose_name="主讲人简介")
    speech_introduction = models.TextField(verbose_name="讲座简介")
    speech_time = models.TextField(verbose_name="讲座时间")
    speech_place = models.TextField(verbose_name="讲座地点")
    speech_capacity = models.IntegerField(verbose_name="讲座容量")
    speech_chair_remain_number = models.IntegerField(verbose_name="讲座座位剩余数量")
    speech_add_time = models.DateTimeField(auto_now_add=True, verbose_name="讲座添加时间")

    # def __str__(self):
    #     return self.speech_name +" - "+ self.speech_speaker_name +" - "+ self.speech_time +" - "+ self.speech_place
    
    class Meta:
        verbose_name_plural = "讲座"
        verbose_name = "讲座"
        ordering = ['-speech_add_time']


class Student(models.Model):
    stu_number = models.TextField(verbose_name="账号ID")
    stu_name = models.TextField(verbose_name="学生姓名")
    stu_college = models.TextField(verbose_name="学生所在学校")
    stu_class = models.TextField(verbose_name="学生所在班级")
    stu_phone_number = models.TextField(verbose_name="学生电话号码")

    # def __str__(self):
    #     return self.stu_number +" - "+ self.stu_name +" - "+ self.stu_college +" - "+ self.stu_class +" - "+ self.stu_phone_number

    class Meta:
        verbose_name_plural = "学生"
        verbose_name = "学生"
        ordering = ["stu_number"]


class BookingOrder(models.Model):
    order_speech_id = models.IntegerField(verbose_name="订单指定的讲座号")
    order_stu_number = models.TextField(verbose_name="账号ID")
    order_time = models.DateTimeField(auto_now_add=True, verbose_name="订单建立时间")
    order_stu_phone_number = models.TextField(verbose_name="学生电话号码")
    order_stu_name = models.TextField(verbose_name="学生姓名")
    # Speech.objects.get("id=order_speech_id").speech_name
    # def __str__(self):
    #     return "{} - {} - {} - {} - {}".format(str(self.order_time), 
    #         Speech.objects.get(id=self.order_speech_id).speech_name, 
    #         self.order_stu_number, 
    #         self.order_stu_name,
    #         self.order_stu_phone_number) 

    class Meta:
        verbose_name_plural = "订单"
        verbose_name = "订单"
        ordering = ["-order_time"]
    
from django.db import models

# Create your models here.
class People(models.Model):
    #创建了一个People的表
    name = models.CharField(null=True,blank=True,max_length=200)
    #允许name为空，允许为空白，最大长度不超过200
    job = models.CharField(null=True,blank=True,max_length=200)

from django.db import models

# 公共字段表
# Create your models here.
class CommonInfo(models.Model):
    name=models.CharField(max_length=100,unique=True,verbose_name="名称")
    description=models.CharField(max_length=100,blank=True,null=True,verbose_name="描述")
    change_date=models.DateTimeField(auto_now=True)     #改变时，更改时间
    add_date=models.DateTimeField(auto_now_add=True)   #添加时间
    status=models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract=True
        ordering=('-change_date',)

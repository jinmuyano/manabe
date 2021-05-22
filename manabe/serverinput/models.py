from django.db import models
from django.contrib.auth.models import User
from appinput.models import App
from envx.models import Env
from public.models import CommonInfo

# Create your models here.

class Server(CommonInfo):
    """
    服务器
    """
    # 服务器ip地址
    ip_address=models.CharField(max_length=24,verbose_name="IP地址")

    # salt agent名称
    salt_name=models.CharField(max_length=128,verbose_name="SaltStack minion")

    # 服务器上app对应的端口号
    port=models.CharField(max_length=100,verbose_name="端口")

    # 服务器对应的所有app应用
    app_name=models.ForeignKey(App,related_name='app_name',on_delete=models.CASCADE,verbose_name="应用名")

    env_name=models.ForeignKey(Env,blank=True,null=True,related_name="server_env_name",on_delete=models.CASCADE,verbose_name="环境")

    # 服务启动用户，root或者其他
    app_user=models.CharField(max_length=24,blank=True,null=True,verbose_name="执行程序用户")

    # 谁进行了app操作
    op_user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,verbose_name="操作用户")

    # 服务器已部署多少个发布单，回滚时需要
    history_deploy=models.CharField(max_length=512,blank=True,null=True,verbose_name="已部署版本")

    deploy_status=models.CharField(max_length=128,null=True,blank=True,verbose_name="发布状态(Err,Suc)")

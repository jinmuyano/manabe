### 基础配置

##### 安装软件

```sh
#服务器配置虚拟环境
mkdir manabe
cd manabe
pip3 install pipenv 
pipenv shell


#安装包
(manabe) root@database:~/devops/manabe# cat requirements.txt 
channels==2.1.4
Django==2.1.3
djangorestframework==3.9.0
gunicorn==19.9.0
PyMySQL==0.9.2
python-jenkins==1.4.0
Twisted==18.9.0
uWSGI==2.0.17.1

pip3 install -r requirements.txt 
```





##### 创建django项目

```sh
D:\github\python-manabe>django-admin startproject manabe

D:\github\python-manabe>cd manabe

D:\github\python-manabe\manabe>python manage.py startapp serverinput

D:\github\python-manabe\manabe>python manage.py startapp appinput

D:\github\python-manabe\manabe>python manage.py startapp deploy

D:\github\python-manabe\manabe>python manage.py startapp envx

D:\github\python-manabe\manabe>python manage.py startapp rightadmin

D:\github\python-manabe\manabe>python manage.py startapp public
```

##### 修改settings.py

```python
#注释
'''
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
'''

# 语言
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'


ALLOWED_HOSTS = ['*']

# 数据库使用mysql
DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.mysql',

        'NAME':'manabe',

        'USER':'root',

        'PASSWORD':'123',

        'HOST': '192.168.157.49',

        'PORT': '3306',
    }
}

# 注册app,将上面创建的app注册进去，不然数据库下models等代码迁移不生效
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'public.apps.PublicConfig',
    'appinput.apps.AppinputConfig',
    'deploy.apps.DeployConfig',
    'envx.apps.EnvxConfig',
    'rightadmin.apps.RightadminConfig',
    'serverinput.apps.ServerinputConfig',
    'api.apps.ApiConfig',
]
```

##### 数据库配置

```sql
# 安装数据库省略
create database manabe;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123';
flush privileges;
exit
```

#####  配置pycharm远程提交代码

[PyCharm 配置远程python解释器](https://www.cnblogs.com/sddai/p/9648211.html)



##### 数据库迁移

```sh
# 修改python引擎
(manabe) root@database:~/devops/manabe/manabe# cat  manabe/__init__.py   
import pymysql
pymysql.install_as_MySQLdb()

# 服务器操作
(manabe) root@database:~/devops/manabe/manabe# python manage.py  makemigrations
(manabe) root@database:~/devops/manabe/manabe# python manage.py  migrate

# 创建超级用户
(manabe) root@database:~/devops/manabe/manabe# python manage.py  createsuperuser
用户名 (leave blank to use 'root'): admin

# 测试访问
(manabe) root@database:~/devops/manabe/manabe# python manage.py runserver 0.0.0.0:5000
```

##### url路由调整

```python
#主app-manabe下修改如下
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [path('app/',include('appinput.urls')),]
urlpatterns += [path('deploy/',include('deploy.urls')),]
urlpatterns += [path('envx/',include('envx.urls')),]
urlpatterns += [path('public/',include('public.urls')),]
urlpatterns += [path('rightadmin/',include('rightadmin.urls'))]
urlpatterns += [path('server/',include('serverinput.urls'))]


# 每个子app添加urls文件，并写入
from django.urls import path
app_name='appinput'  #对应名称更改
urlpatterns=[]
```



### models

##### public models.py

公共字段表

```python
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
        abstract=True   #定义为抽象表
        ordering=('-change_date0',)
```

##### appinput models.py

应用数据表

```python
from django.db import models
from django.contrib.auth.models import User  #使用django自带的用户model
from public.models import CommonInfo

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# 应用数据表
# 每当创建新用户并将其保存到数据库时，就会触发此代码
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

class App(CommonInfo):
    """
    应用
    """
    jenkins_job=models.CharField(max_length=255,verbose_name="JENKINS JOB名称")
    git_url=models.CharField(max_length=512,verbose_name="Git地址")
    dir_build_file=models.CharField(max_length=512,verbose_name="编译目录")
    build_cmd=models.CharField(max_length=512,default="./",verbose_name="编译命令")
    is_restart_status=models.BooleanField(default=True,verbose_name="是否重启")
    package_name=models.CharField(max_length=128,blank=True,null=True,verbose_name="软件包名")
    zip_package_name=models.CharField(max_length=128,blank=True,null=True,verbose_name="压缩包名")
    op_log_no=models.IntegerField(blank=True,null=True,default=0)  #记录服务启动停止操作次数
    manage_user=models.ForeignKey(User,blank=True,null=True,related_name="manager_user",on_delete=models.CASCADE,verbose_name="APP管理员") #models.CASCADE：删除主表数据，从表数据也会删除
    script_url=models.CharField(max_length=128,blank=True,null=True,verbose_name="app脚本链接")


    def __str__(self):
        return self.name

    class Meta:
        db_table= 'App'
        ordering=('-add_date',)
```

##### 执行数据库迁移

```sh
python manage.py makemigrations
python manage.py migrate     #数据库创建App表
python manage.py  createsuperuser   #用户admin，密码123
```

##### appinput models注册到admin

```python
# 更改appinput/admin.py 将数据表注册到后台页面
from django.contrib import admin
# Register your models here.
from . import models
admin.site.register(models.App)


python manage.py runserver 0.0.0.0:5000   #启动服务，查看后台，使用创建的超级用户密码
```

##### 生成模拟数据

```sh
# 创建目录和文件
(manabe) root@database:~/devops/manabe/manabe/public# tree management/
management/
├── commands
│   ├── fake_app.py    #修改model-App表数据
│   ├── fake_data.py   #main文件，从此处调用其他文件修改数据
│   ├── fake_user.py   #修改model-user表数据
│   └── __init__.py    #空文件
└── __init__.py    #空文件





# fake_user.py 文件
from django.contrib.auth.models import User,Group   #导入django自带的model（用户表）

def fake_user_data():
    User.objects.all().delete()   #清除所有用户
    Group.objects.all().delete()   #清除所有用户组
    print("delete all user data")
    User.objects.create_user(username='Dylan', password="password")
    User.objects.create_user(username='Tyler', password="password")
    User.objects.create_user(username='Kyle', password="password")
    User.objects.create_user(username='Dakota', password="password")
    User.objects.create_user(username='Marcus', password="password")
    User.objects.create_user(username='Samantha', password="password")
    User.objects.create_user(username='Kayla', password="password")
    User.objects.create_user(username='Sydney', password="password")
    User.objects.create_user(username='Courtney', password="password")
    User.objects.create_user(username='Mariah', password="password")
    User.objects.create_user(username='tom', password="password")
    User.objects.create_user(username='mary', password="password")
    admin = User.objects.create_superuser('admin','admin@demon.com','admin')   #创建超级用户
    root = User.objects.create_superuser('root','root@demon.com','root')     #创建超级用户
    admin_group=Group.objects.create(name='admin')      #创建一个admin用户组
    Group.objects.create(name='test')      #建立3个用户组
    Group.objects.create(name='dev')
    Group.objects.create(name='operate')
    admin_users=[admin,root]
    admin_group.user_set.set(admin_users)   #将2个超级用户加入admin组
    print('create all user data')
    
 
 
    
# fake_app.py 文件
from random import choice
from django.contrib.auth.models import User
from appinput.models import App

def fake_app_data():
    App.objects.all().delete()
    print('delete all app data')
    user_set = User.objects.all()
    app_list = ['ABC-FRONT-APP-ADMIN',
                'ABC-FRONT-APP-NGINX',
                'ABC-FRONT-APP-VUEJS',
                'ABC-FRONT-APP-ANGULAR',
                'ABC-FRONT-APP-BOOTSTRAP',
                'ABC-BACKEND-NODEJS',
                'ABC-BACKEND-JAVA',
                'ABC-BACKEND-GO',
                'ABC-BACKEND-PYTHON',
                'ABC-BACKEND-SCALA',
                'ZEP-FRONT-APP-ADMIN',
                'ZEP-FRONT-APP-NGINX',
                'ZEP-FRONT-APP-VUEJS',
                'ZEP-FRONT-APP-ANGULAR',
                'ZEP-FRONT-APP-BOOTSTRAP',
                'ZEP-BACKEND-NODEJS',
                'ZEP-BACKEND-JAVA',
                'ZEP-BACKEND-GO',
                'ZEP-BACKEND-PYTHON',
                'ZEP-BACKEND-SCALA',
                ]
    for app_item in app_list:
        App.objects.create(name=app_item, jenkins_job=app_item, git_url="http://localhost", build_cmd="mvn package",
                           package_name=app_item + '.zip', manage_user=choice(user_set))
    print('create all app data')
    
    
    
    
    
#fake_data.py 文件
from django.core.management.base import BaseCommand
from .fake_user import fake_user_data
from .fake_app import fake_app_data

class Command(BaseCommand):
    help= 'It is a fake command,Import init data for test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin fake data'))
        fake_user_data()
        fake_app_data()
        # fake_env_data()
        # fake_server_data()
        # fake_deploy_status_data()
        # fake_deploy_data()
        # fake_action_data()
        # fake_permission_data()
        self.stdout.write(self.style.SUCCESS("end fake data"))
```

envx models.py

环境数据表

```python
```


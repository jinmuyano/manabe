"""manabe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views  # 密码重置路由
from .views import IndexView,user_register, user_login
from public.verifycode import verify_code   #验证码
from django.contrib.auth.views import logout_then_login
from rest_framework.authtoken import views
from .password_views import change_email, change_password


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(IndexView.as_view()), name="index"),
    path('accounts/register/', user_register, name='register'),
    path('accounts/login/', user_login, name='login'),
    path('verify_code/', verify_code, name='verify_code'),
]

# 邮箱修改
urlpatterns += [path('accounts/change_email/', login_required(change_email), name="change_email"), ]

# 密码更改
urlpatterns += [path('accounts/change_password/', login_required(change_password), name="change_password"), ]

# 密码重置路由
# PasswordResetView生成一次性链接，发给用户注册时填写的邮箱，让用户重置密码,如果数据库没有该用户，该视图也不会发邮件
# password_reset.html 显示密码重设表单
# email_template_name用户生成带有密码重设链接的电子邮件
# subject_template_name 用于生成密码重设邮件的主题
urlpatterns += [path('reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',
                                                                    email_template_name='accounts/password_reset_email.html',
                                                                    subject_template_name='accounts/password_reset_subject.txt'),
                     name='password_reset'), ]

# 成功把密码重设链接发给用户后，显示的页面
urlpatterns += [
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'), ]

# 输入新密码的表单
urlpatterns += [path('reset/<uidb64>/<token>/',
                     auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
                     name='password_reset_confirm'), ]

# 告诉用户成功修改了密码
urlpatterns += [path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
    template_name='accounts/password_reset_complete.html'), name='password_reset_complete'), ]

# 模块路由
urlpatterns += [path('app/', include('appinput.urls')), ]
urlpatterns += [path('deploy/', include('deploy.urls')), ]
urlpatterns += [path('envx/', include('envx.urls')), ]
urlpatterns += [path('public/', include('public.urls')), ]
urlpatterns += [path('rightadmin/', include('rightadmin.urls')), ]
urlpatterns += [path('server/', include('serverinput.urls')), ]

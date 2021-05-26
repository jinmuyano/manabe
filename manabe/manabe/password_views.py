from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .forms import ChangeEmailForm,ChangepwdForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate   #验证账户是否存在


@require_http_methods(['GET','POST'])
def change_email(request):
    if request.method == 'GET':
        form=ChangeEmailForm()
        return render(request,'accounts/change_email.html',
                      {'form':form,'current_page_name':'更改邮箱','email':User.objects.get(username=request.user.username).email,})
    else:
        error=[]
        form=ChangeEmailForm(request.POST)
        # 判断是否通过验证
        if form.is_valid():
            #通过验证，修改邮箱
            username=request.user.username
            new_email1=request.POST.get('new_email1')
            User.objects.filter(username=request.user.username).update(email=new_email1)
            email=User.objects.get(username=request.user.username).email
            change_email_success=True
            return render(request,'accounts/change_email.html',locals())
        else:
            # 未通过验证
            error.append('两次新邮箱不匹配,或是邮箱格式错误,请重新输入')
            email=User.objects.get(username=request.user.username).email
            return render(request, 'accounts/change_email.html', locals())


# 修改密码视图
@require_http_methods(['GET','POST'])
def change_password(request):
    if request.method == 'GET':
        form=ChangepwdForm()
        return render(request,'accounts/change_password.html',{'form':form,'changepwd_success':True})
    else:
        error=[]
        form=ChangepwdForm(request.POST)
        if form.is_valid():
            # 判断原密码是否正确
            username=request.user.username
            oldpassword=request.POST.get('oldpassword','')
            user=authenticate(username,oldpassword)  #如果验证通过返回user对象，如果验证失败返回none
            if user is not None and user.is_active:
                #修改密码
                newpassword1=request.POST.get('newpassword1','')
                user.set_password(newpassword1)
                user.save()
                return render(request, 'accounts/change_password.html',{'changepwd_success':True})
            else:
                error.append('原密码错误')
                return render(request,'accounts/change_password.html',locals())

        else:
            #两次密码不匹配
            error.append('两次密码不一致')
            return render(request,'accounts/change_password.html',locals())


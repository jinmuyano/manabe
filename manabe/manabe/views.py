#首先导入系统库,再导入框架库,最后导入用户库
import platform
import django
from django.views.generic.base import TemplateView
from django.shortcuts import render,HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate,login     #判断是否存在该用户
from django.urls import reverse
from django.contrib.auth.models import User
from appinput.models import App
from serverinput.models import Server
from deploy.models import DeployPool
from .forms import LoginForm,RegisterForm   #自己定义的表单




class IndexView(TemplateView):
    template_name = "manabe/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   #向网页模板传递更多上下文
        context['current_page'] = "index"
        context['app_count'] = App.objects.count()
        context['server_count'] = Server.objects.count()
        context['deploy_count'] = DeployPool.objects.count()
        context['REMOTE_ADDR'] = self.request.META.get("REMOTE_ADDR")
        context['HTTP_USER_AGENT'] = self.request.META.get("HTTP_USER_AGENT")
        context['HTTP_ACCEPT_LANGUAGE'] = self.request.META.get("HTTP_ACCEPT_LANGUAGE")
        context['platform'] = platform.platform()
        context['python_version'] = platform.python_version()
        context['django_version'] = django.get_version()

        return context

# 重定向到登录页面
def redirect_login(request):
    login_url = reverse('index')
    return HttpResponseRedirect(request.Post.get('next',login_url) or login_url)   #如果or左边为true则使用or左边，如果or左边为false则使用or右边



# 用户登录
@require_http_methods(["GET", "POST"])
def user_login(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        vc = request.POST['vc']
        if vc.upper() != request.session['verify_code']:
            error.append('验证码错误！')
            return render(request, "accounts/login.html", locals())
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect_login(request)
            else:
                error.append('请输入正确的用户名和密码')
                return render(request, "accounts/login.html", locals())
        else:
            return render(request, "accounts/login.html", locals())
    else:
        form = LoginForm()
        return render(request, "accounts/login.html", locals())



# 用户注册视图
@require_http_methods(["GET","POST"])
def user_register(request):
    error=[]
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data   #取出通过表单验证的数据
            username=data['username']
            email=data['email']
            password=data['password']
            password2=data['password2']
            if not User.objects.all().filter(username__iexact=username):    #如果用户不存在则为true,iexact=ilike
                if form.pwd_validate(password,password2):    #调用form中验证password和password2是否一致
                    user=User.objects.create_user(username=username,password=password,email=email)
                    user.save()
                    user=authenticate(username=username,password=password)   #判断用户的密码是否有效，有效返回用户对象，无效返回none
                    login(request,user)  #
                    return redirect_login(request)   #调用上面的方法，重定向到首页
                else:
                    error.append("密码不一致，请确认")
            else:
                error.append('已存在相同用户名，请更换用户名')
        else:
            error.append('请确认各个输入框无误')
            return render(request, 'accounts/register.html', locals())
    else:
        form=RegisterForm()
        return render(request,'accounts/register.html',locals())  #第一次请求返回空的form表单



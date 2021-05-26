from django import forms


# 用户登录
class LoginForm(forms.Form):
    username = forms.CharField(required=True, label=u"用户名", error_messages={'required': u'请输入用户名'},
                               widget=forms.TextInput(
                                   attrs={'placeholder': u'账号', 'rows': '1', 'class': 'input-text size-L'}),)  #用户名输入框属性
    password= forms.CharField(required=True,label=u"密码",error_messages={'required':u'请输入密码'},
                              widget=forms.PasswordInput(attrs={'placeholder':u"密码",'rows':1,'class':'input-text size-L'}),)


# 用户注册
class RegisterForm(forms.Form):
    username=forms.CharField(required=True,label=u"用户名",error_messages={'required':u'请输入用户名'},
                             widget=forms.TextInput(attrs={'placeholder':u'账号','rows':'1','class':'input-text size-L'}),)

    email=forms.EmailField(required=True,label='邮箱',error_messages={'required':u'请输入电子邮箱'},
                           widget=forms.TextInput(attrs={'placeholder':u'此邮箱用户密码找回','rows':1,'class':'input-text size-L'}))

    password=forms.CharField(required=True,error_messages={'required':u'请输入密码'},
                             widget=forms.PasswordInput(attrs={'placeholder':u'请输入密码','rows':1,'class':'input-text size-L'}))

    password2=forms.CharField(required=True,label='Confirm',error_messages={'required':u'请再次输入密码'},
                             widget=forms.PasswordInput(attrs={'placeholder':u'请输入密码','rows':1,'class':'input-text size-L'}))

    # 验证2次密码是否一致,views视图调用
    def pwd_validate(self,p1,p2):
        return p1==p2


# 更改邮箱表单
class ChangeEmailForm(forms.Form):
    new_email1=forms.EmailField(required=True,label=u"新邮箱地址",error_messages={'required':u'请输入新邮箱地址'},
                                widget=forms.TextInput(attrs={'placeholder':u"请输入新邮箱地址","rows":1,"class":'input-text size-L'}))
    new_email2=forms.EmailField(required=True,label=u"新邮箱地址",error_messages={'required':u'请输入新邮箱地址'},
                                widget=forms.TextInput(attrs={'placeholder':u"请输入新邮箱地址","rows":1,"class":'input-text size-L'}))

    # 自动被调用
    # 重写父类的方法clean,form表单调用顺序是init>clean>Validate>save
    # 在clean方法中，增加其他验证功能
    def clean(self):
        print(self.cleaned_data,"%%%%%%%%%%%%%%%%%%%")
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['new_email1'] != self.cleaned_data['new_email2']:
            print("*************************")
            raise forms.ValidationError("两次输入的邮箱地址不一致")
        else:
            cleaned_data =super(ChangeEmailForm,self).clean()
        return cleaned_data   #clean方法必须返回data


# 更改密码表单
class ChangepwdForm(forms.Form):
    oldpassword=forms.CharField(required=True,label=u"原密码",error_messages={'required':u'请输入原密码'},
                                widget=forms.PasswordInput(attrs={'row':1,'placeholder':u"原密码","class":'input-text size-L'}))

    newpassword1=forms.CharField(required=True,label=u"新密码",error_messages={'required':u'请输入新密码'},
                                 widget=forms.PasswordInput(attrs={'row':1,'placeholder':u"新密码","class":'input-text size-L'}))

    newpassword2=forms.CharField(required=True,label=u"确认密码",error_messages={'required':u'请再次输入新密码'},
                                 widget=forms.PasswordInput(attrs={'row': 1, 'placeholder': u"确认密码", "class": 'input-text size-L'}))
    def clean(self):
        print(self.cleaned_data,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        if not self.is_vaild():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            print("*****************************")
            raise forms.ValidationError(u"两次输入密码不同")
        else:
            cleaned_data=super().clean()
        return cleaned_data
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile, EmailVerifyCode


class UserRegisterForm(forms.Form):
    # 邮箱格式验证
    email = forms.EmailField(required=True)
    # 密码格式验证
    password = forms.CharField(required=True, min_length=3, max_length=15,
                               error_messages={
                                   'required': '密码必须填写',
                                   'min_length': '密码至少三位',
                                   'max_length': '密码不能超过15位'
                               })
    # 验证码
    captcha = CaptchaField()


class UserLoginForm(forms.Form):
    # 邮箱格式验证
    email = forms.EmailField(required=True)
    # 密码格式验证
    password = forms.CharField(required=True, min_length=3, max_length=15,
                               error_messages={
                                   'required': '密码必须填写',
                                   'min_length': '密码至少三位',
                                   'max_length': '密码不能超过15位'
                               })


class UserForgetForm(forms.Form):
    # 邮箱格式验证
    email = forms.EmailField(required=True)
    # 验证码
    captcha = CaptchaField()


class UserResetForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=3, max_length=15,
                                error_messages={
                                    'required': '密码必须填写',
                                    'min_length': '密码至少三位',
                                    'max_length': '密码不能超过15位'
                                })
    password2 = forms.CharField(required=True, min_length=3, max_length=15,
                                error_messages={
                                    'required': '密码必须填写',
                                    'min_length': '密码至少三位',
                                    'max_length': '密码不能超过15位'
                                })


class UserChangeImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'address', 'phone', 'birthday']


class UserChangeEmailForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyCode
        fields = ['email']


class UserResetEmailForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyCode
        fields = ['email', 'code']


class UserPwdForm(forms.Form):
    pwd = forms.CharField(required=True, min_length=3, max_length=15,
                          error_messages={
                              'required': '密码必须填写',
                              'min_length': '密码至少三位',
                              'max_length': '密码不能超过15位'
                          })
    repwd = forms.CharField(required=True, min_length=3, max_length=15,
                            error_messages={
                                'required': '密码必须填写',
                                'min_length': '密码至少三位',
                                'max_length': '密码不能超过15位'
                            })

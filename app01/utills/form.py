from django import forms
from django.core.validators import RegexValidator
from django.urls import reverse

from app01 import models


class LoginForm(forms.Form):
    name = forms.CharField(
        label="用户名",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        label="密码",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        )
    )


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
    )

    password = forms.CharField(
        label="密码",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        )
    )


class UserAddModelForm(forms.ModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )
    name = forms.CharField(
        label="姓名",
        validators=[RegexValidator(r'^(\u4e00-\u9fa5)*', "姓名输入错误，请输入中文")]
    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'create_time', 'gender', 'dorm', 'mobile']


class UserEditForm(UserAddModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'age', 'create_time', 'gender', 'dorm', 'mobile']


class DormForm(forms.ModelForm):
    admin_mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.DormInfo
        fields = '__all__'


# 文章添加form
class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = models.ArticlePost
        fields = ['title', 'body']

    def get_absolute_url(self):
        return reverse('/article/detail/', kwargs=[self.id])


# 评论form
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body']


"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import notifications.urls
from django.urls import path
from django.conf.urls import include
from app01 import views

app_name = "admin"
urlpatterns = [
    # 测试界面,可以绕过中间件（不用登陆）。仅作为测试功能用
    path('test/', views.test),

    # 登录界面
    path('login/', views.login),
    path('admin/login/', views.admin_login),
    path('logout/', views.logout, name='logout'),
    path('image/code/', views.verifycode),

    # 主界面（各类表格）
    # 用户表的相关url以及view
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/<int:nid>/delete/', views.user_delete),
    path('user/<int:nid>/edit/', views.user_edit),

    # 宿舍表的相关url以及view
    path('dorm/add/', views.dorm_add),
    path('dorm/list/', views.dorm_list),
    path('dorm/find/lowE/', views.dorm_find_lowE),
    path('dorm/back/', views.dorm_back),
    path('dorm/<int:nid>/delete/', views.dorm_delete),
    path('dorm/<int:nid>/edit/', views.dorm_edit),

    # 管理人员的相关url以及views
    path('admin/list/', views.admin_list),

    # 留言板相关的url以及views
    path('article/list/', views.article_list),
    path('article/<int:nid>/detail/', views.article_detail),
    path('article/<int:nid>/delete/', views.article_delete),
    path('article/<int:nid>/edit/', views.article_edit),
    path('article/add/', views.article_add),

    # 评论模块相关的url以及views
    path('post/comment/<int:nid>', views.post_comment, name='comment'),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

import io
import random
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from app01.utills.Pagination import Pagination
from app01.utills.form import *

from notifications.signals import notify

def admin_login(request):
    # 管理员登陆界面
    if request.method == "GET":
        form = AdminLoginForm()
        return render(request, 'admin_login.html', {'form': form})

    # 如果是post请求
    else:
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            user_obj = models.admin.objects.filter(**form.cleaned_data).first()
            # 如果密码正确，并且是用户
            # 则需要写入到cookie和session中
            if models.admin.objects.filter(**form.cleaned_data).exists():
                # 如果验证码也输入正确，写入cookie和session
                if request.session["verifycode"] == request.POST.get("code"):
                    request.session["info"] = {'id': user_obj.id, "name": user_obj.username}
                    return redirect("/user/list")
                # 密码正确但是验证码错误
                else:
                    form.add_error("password", "验证码输入错误")
                    return render(request, 'admin_login.html', {'form': form})
            # 如果密码错误
            else:
                form.add_error("username", "用户名或密码错误")
                return render(request, 'admin_login.html', {'form': form})
        # 如果form中的元素不合规
        return render(request, 'admin_login.html', {'form': form})


def login(request):
    # 如果是get请求
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    # 如果是post请求
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user_obj = models.UserInfo.objects.filter(**form.cleaned_data).first()
            # 如果密码正确，并且是用户
            # 则需要写入到cookie和session中
            if models.UserInfo.objects.filter(**form.cleaned_data).exists():
                # 如果验证码也输入正确，写入cookie和session
                if request.session["verifycode"] == request.POST.get("code"):
                    request.session["info"] = {'id': user_obj.id, "name": user_obj.name}
                    return redirect("/user/list")
                # 密码正确但是验证码错误
                else:
                    form.add_error("password", "验证码输入错误")
                    return render(request, 'login.html', {'form': form})
            # 如果密码错误
            else:
                form.add_error("name", "用户名或密码错误")
                return render(request, 'login.html', {'form': form})
        # 如果form中的元素不合规
        return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect("/login/")


def verifycode(request):
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画布
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点

    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fi = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fi)

    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    font = ImageFont.truetype("C:\Windows\Fonts\Gadugi.ttf", 40)
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))

    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    del draw

    request.session['verifycode'] = rand_str

    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue())


def test(request):
    return render(request, 'test.html')


def user_list(request):
    queryset = models.UserInfo.objects.all()
    page_obj = Pagination(request, queryset, page_size=10)
    page_queryset = page_obj.page_query
    page_str = page_obj.html()

    # 如果page有传递参数进来
    if request.GET.get('page'):
        # prev_url:处理的是分页系统中向前一页。
        # for_url处理的是分页系统中向后一页
        prev_url = '/user/list/?page={}'.format(int(request.GET.get('page')) - 1)
        for_url = '/user/list/?page={}'.format(int(request.GET.get('page')) + 1)
        return render(request, 'user_list.html',
                      {'queryset': page_queryset, 'page_str': page_str, 'prev_url': prev_url, 'for_url': for_url})
    # 没有page参数
    return render(request, 'user_list.html', {'queryset': page_queryset, 'page_str': page_str})


def user_add(request):
    if request.method == "GET":
        form = UserAddModelForm()
        return render(request, 'user_add.html', {"form": form})
    # 提交数据，需要校验
    else:
        form = UserAddModelForm(data=request.POST)
        if form.is_valid():
            # 如果数据合法，保存到数据库
            print(form.cleaned_data)
            # 自动保存，定义在哪个类就放在哪个类
            form.save()
            return redirect("/user/list/")
        else:
            # 校验失败
            print(form.errors)
            # 这里的form和初始的form不太相同，此处的form有data存在，若验证失败，还有错误信息
            return render(request, 'user_add.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def user_edit(request, nid):
    if request.method == "GET":
        # 根据id去数据库获取要编辑的那行数据
        row_obj = models.UserInfo.objects.filter(id=nid).first()
        # 只需要将本行对象传入form，并且加一个instance=，那么form就会自动将所有信息填充在提交框中
        form = UserEditForm(instance=row_obj)
        return render(request, 'user_edit.html', {"form": form})
    else:
        # 在编辑中，需要告诉modelform到底是编辑哪一行数据，否则就会直接将数据添加在数据库中
        # 具体做法就是首先获取到数据后再将instance=row_obj装入
        row_object = models.UserInfo.objects.filter(id=nid).first()
        form = UserEditForm(data=request.POST, instance=row_object)  # 比添加多一个instance=rowobject
        if form.is_valid():
            form.save()
            return redirect("/user/list")
        else:
            return render(request, 'user_edit.html', {'form': form})


def dorm_list(request):
    queryset = models.DormInfo.objects.all()
    page_obj = Pagination(request, queryset, page_size=10)
    page_queryset = page_obj.page_query
    page_str = page_obj.html()

    # 如果page有传递参数进来
    if request.GET.get('page'):
        # prev_url:处理的是分页系统中向前一页。
        # for_url处理的是分页系统中向后一页
        prev_url = '/dorm/list/?page={}'.format(int(request.GET.get('page')) - 1)
        for_url = '/dorm/list/?page={}'.format(int(request.GET.get('page')) + 1)
        return render(request, 'dorm_list.html',
                      {'queryset': page_queryset, 'page_str': page_str, 'prev_url': prev_url, 'for_url': for_url})
    return render(request, 'dorm_list.html', {'queryset': page_queryset, 'page_str': page_str})


def dorm_find_lowE(request):
    # 快速找到电费低于100的视图函数
    conditions = {'electric_charge__lt': 100}
    queryset = models.DormInfo.objects.filter(**conditions).all()
    page_obj = Pagination(request, queryset, page_size=10)
    page_queryset = page_obj.page_query
    page_str = page_obj.html()
    return render(request, 'dorm_list.html', {'queryset': page_queryset, 'page_str': page_str})


def dorm_back(request):
    return redirect("/dorm/list/")


def dorm_delete(request, nid):
    models.DormInfo.objects.filter(id=nid).delete()
    return redirect("/dorm/list/")


def dorm_add(request):
    if request.method == "GET":
        form = DormForm()
        return render(request, 'dorm_add.html', {"form": form})
    # 提交数据，需要校验
    else:
        form = DormForm(data=request.POST)
        if form.is_valid():
            # 如果数据合法，保存到数据库
            print(form.cleaned_data)
            # 如果实际在校人数逻辑不符
            if form.cleaned_data['accom_num'] < form.cleaned_data['on_canpus_num']:
                form.add_error('on_canpus_num', "请注意实际在校人数是否正确")
                return render(request, 'dorm_add.html', {"form": form})
            # 自动保存，定义在哪个类就放在哪个类
            form.save()
            return redirect("/dorm/list/")
        else:
            # 校验失败
            print(form.errors)
            # 这里的form和初始的form不太相同，此处的form有data存在，若验证失败，还有错误信息
            return render(request, 'dorm_add.html', {"form": form})


def dorm_edit(request, nid):
    if request.method == "GET":
        # 根据id去数据库获取要编辑的那行数据
        row_obj = models.DormInfo.objects.filter(dorm_id=nid).first()
        # 只需要将本行对象传入form，并且加一个instance=，那么form就会自动将所有信息填充在提交框中
        form = DormForm(instance=row_obj)
        return render(request, 'user_edit.html', {"form": form})
    else:
        # 在编辑中，需要告诉modelform到底是编辑哪一行数据，否则就会直接将数据添加在数据库中
        # 具体做法就是首先获取到数据后再将instance=row_obj装入
        row_object = models.DormInfo.objects.filter(dorm_id=nid).first()
        form = DormForm(data=request.POST, instance=row_object)  # 比添加多一个instance=row_object
        if form.is_valid():
            form.save()
            return redirect("/dorm/list")
        else:
            return render(request, 'user_edit.html', {'form': form})


def admin_list(request):
    login_info = request.session['info']
    condition = {'username': login_info['name']}
    if models.admin.objects.filter(**condition).exists():
        # 如果判定为是管理员进行的登陆
        queryset = models.admin.objects.all()
        page_obj = Pagination(request, queryset, page_size=10)
        page_queryset = page_obj.page_query
        page_str = page_obj.html()

        # 如果page有传递参数进来
        if request.GET.get('page'):
            # prev_url:处理的是分页系统中向前一页。
            # for_url处理的是分页系统中向后一页
            prev_url = '/admin/list/?page={}'.format(int(request.GET.get('page')) - 1)
            for_url = '/admin/list/?page={}'.format(int(request.GET.get('page')) + 1)
            return render(request, 'admin_list.html',
                          {'queryset': page_queryset, 'page_str': page_str, 'prev_url': prev_url, 'for_url': for_url})
        return render(request, 'admin_list.html', {'queryset': page_queryset, 'page_str': page_str})
    # 如果不是管理员的登陆
    messages.warning(request, '您似乎不是管理员，此项功能只有管理员才可以使用')
    return redirect("/user/list/")


def decide_order(order):
    # 防止article_list 中order为None
    if order is None:
        return 1
    else:
        return order


def article_list(request):
    # order为1 指的是默认为按照发布时间分类。order为2 指的是按照最热分类。
    order = request.GET.get('order')

    # search指的是用户是否在搜索框中输入了什么
    search = request.GET.get('search')

    if search:
        # 如果用户使用了搜索
        if order == "2":
            queryset = models.ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            queryset = models.ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将search置空，防止重置NONE
        search = ''
        order = ''
        if order == "2":
            queryset = models.ArticlePost.objects.all().order_by('-total_views')
        else:
            queryset = models.ArticlePost.objects.all()
    # 实例化分页
    page_obj = Pagination(request, queryset, page_size=9)
    page_queryset = page_obj.page_query
    page_str = page_obj.html()
    # 如果url中有页码
    if request.GET.get('page'):
        if request.GET.get("order"):
            # 如果用户选择了order
            context = {'queryset': page_queryset,
                       'page_str': page_str,
                       'prev_url': '/article/list/?page={}&order={}&search={}'.format(
                           max(int(request.GET.get('page')) - 1, 0),
                           order, search),
                       'for_url': '/article/list/?page={}&order={}&search={}'.format(
                           max(int(request.GET.get('page')) + 1, 0),
                           order, search),
                       'search': search
                       }
            return render(request, 'article_list.html', context)
        else:
            # 用户没有选择order
            context = {'queryset': page_queryset,
                       'page_str': page_str,
                       'prev_url': '/article/list/?page={}&order={}&search={}'.format(
                           max(int(request.GET.get('page')) - 1, 0),
                           "1", search),
                       'for_url': '/article/list/?page={}&order={}&search={}'.format(
                           max(int(request.GET.get('page')) + 1, 0),
                           "1", search),
                       'search': search
                       }
            return render(request, 'article_list.html', context)
    # url中没有页码
    context = {'queryset': page_queryset,
               'page_str': page_str,
               'search': search
               }

    return render(request, 'article_list.html', context)


def article_detail(request, nid):
    query = models.ArticlePost.objects.get(id=nid)  # 拿到具体的文章对象
    comments = models.Comment.objects.filter(article=nid)  # 关于此文章的评论
    form = CommentForm()
    # 拿到session用户信息
    login_info = request.session['info']
    info = login_info['id']
    query.total_views += 1
    query.save(update_fields=['total_views'])

    # 需要传递给模板的对象
    page_obj = Pagination(request, comments, page_size=5)
    page_queryset = page_obj.page_query
    page_str = page_obj.html()

    # 如果是post请求
    if request.method == 'POST':
        form = CommentForm(data=request.POST, instance=comments.first())
        models.Comment.objects.create(
            body=form.data['body'],
            created=datetime.now(),
            article_id=nid,
            user_id=info
        )
        return redirect("/article/{}/detail".format(nid))

    # 如果是get请求
    else:
        context = {'page_queryset': page_queryset,
                   'query': query,
                   'info': info,
                   'comments': comments,
                   'form': form,
                   'page_str': page_str}
        return render(request, 'article_detail.html', context)

# def post_comment(request, article_id, parent_comment_id=None):
#     article = get_object_or_404(models.ArticlePost, id=article_id)
#
#     # 处理 POST 请求
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.article = article
#             new_comment.user = request.user
#
#             # 二级回复
#             if parent_comment_id:
#                 parent_comment = models.Comment.objects.get(id=parent_comment_id)
#                 # 若回复层级超过二级，则转换为二级
#                 new_comment.parent_id = parent_comment.get_root().id
#                 # 被回复人
#                 new_comment.reply_to = parent_comment.user
#                 new_comment.save()
#                 return HttpResponse('200 OK')
#
#             new_comment.save()
#             return redirect(article)
#         else:
#             return HttpResponse("表单内容有误，请重新填写。")
#     # 处理 GET 请求
#     elif request.method == 'GET':
#         comment_form = CommentForm()
#         context = {
#             'comment_form': comment_form,
#             'article_id': article_id,
#             'parent_comment_id': parent_comment_id
#         }
#         return render(request, 'article_list.html', context)
#     # 处理其他请求
#     else:
#         return HttpResponse("仅接受GET/POST请求。")


def article_add(request):
    form = ArticlePostForm()
    # 赋值上下文
    context = {'form': form}
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            login_info = request.session['info']
            new_article.author = models.UserInfo.objects.get(id=login_info['id'])
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("/article/list/")
        # 如果数据不合法，返回错误信息
        else:
            form.add_error('title', "添加內容有誤，請重新填寫")
            return render(request, 'article_create.html', context)
    # 如果用户请求获取数据
    else:
        return render(request, 'article_create.html', context)


# 文章的删除

def article_delete(request, nid):
    article = models.ArticlePost.objects.get(id=nid)
    article.delete()
    return redirect("/article/list/")


def article_edit(request, nid):
    article = models.ArticlePost.objects.get(id=nid)
    # 创建表单类实例
    form = ArticlePostForm()
    # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
    context = {'article': article, 'form': form}
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("/article/{}/detail".format(nid))
        # 如果数据不合法，返回错误信息
        else:
            form.add_error("title", "表单输入有误，请重新输入")
            return render(request, 'article_edit.html', context)

    # 如果用户 GET 请求获取数据
    else:
        # 将响应返回到模板中
        return render(request, 'article_edit.html', context)


def post_comment(request, nid):
    return HttpResponse(" m")

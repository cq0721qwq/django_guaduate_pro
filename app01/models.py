from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class admin(models.Model):
    '''管理员表'''
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)


class DormInfo(models.Model):
    '''宿舍具体信息表'''
    dorm_id = models.SmallIntegerField(verbose_name="寝室号", unique=True, primary_key=True)
    accom_num = models.SmallIntegerField(verbose_name="应入住人数", default=0)
    on_canpus_num = models.SmallIntegerField(verbose_name="实际在校人数", default=0)
    administrator = models.CharField(verbose_name="寝室长", max_length=32)
    admin_mobile = models.CharField(verbose_name="寝室长电话号码", max_length=11)
    electric_charge = models.DecimalField(verbose_name="电费余额", max_digits=10, decimal_places=2, default=0)
    level_choices = (
        (1, "一星寝室"),
        (2, "二星寝室"),
        (3, "三星寝室"),
        (4, "优秀寝室"),
        (5, "最佳寝室")
    )
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=1)


# 继承AbstractUser抽象类
class UserInfo(models.Model):
    '''人员表'''
    name = models.CharField(verbose_name='寝室人员姓名', max_length=16)
    password = models.CharField(verbose_name="  密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入寝时间")  # 相比上一行，此行只有年月日，没有时分秒m

    # 部门id，有约束
    # to-表示与哪张表关联 tofield-表示与此表的哪一列关联
    # 使用foreignkey后，django会自动给字段名加一个_id
    # ondelete = models.CASCADE---级联删除
    # ondelete = models.SET_NULL---置空
    # depart = models.ForeignKey(to=Department, to_field="id", on_delete=models.CASCADE)
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    # 外键 链接的是宿舍表
    dorm = models.SmallIntegerField(verbose_name="寝室号", default=111)
    mobile = models.CharField(verbose_name="电话号码", max_length=11, default='00000000000')

    def __str__(self):
        return self.name


class ArticlePost(models.Model):
    '''留言信息表'''

    # 作者
    author = models.ForeignKey("UserInfo", on_delete=models.CASCADE, to_field='id')
    # 文章标题
    title = models.CharField(max_length=100)
    # 正文部分
    body = models.TextField()
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 更新时间
    updated = models.DateTimeField(auto_now=True)
    # 是否已经编辑过
    update_choices = (
        (1, "原始留言"),
        (2, "已编辑")
    )
    is_updated = models.SmallIntegerField(default=1, choices=update_choices)
    # 浏览量
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    '''评论表'''
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    reply_to = models.ForeignKey(
        UserInfo,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="评论的文章id"
    )
    user = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="评论的用户"
    )
    body = RichTextField(verbose_name="评论的文字")
    created = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]

# 原评论留档
# class Comment(models.Model):
#     '''评论表'''
#
#     article = models.ForeignKey(
#         ArticlePost,
#         on_delete=models.CASCADE,
#         related_name='comments',
#         verbose_name="评论的文章id"
#     )
#     user = models.ForeignKey(
#         UserInfo,
#         on_delete=models.CASCADE,
#         related_name='comments',
#         verbose_name="评论的用户"
#     )
#     body = RichTextField(verbose_name="评论的文字")
#     created = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
#
#     class Meta:
#         ordering = ('created',)
#
#     def __str__(self):
#         return self.body[:20]

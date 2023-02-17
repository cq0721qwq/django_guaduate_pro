# Generated by Django 3.2.16 on 2023-02-14 22:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dorminfo',
            name='accom_num',
            field=models.SmallIntegerField(default=0, verbose_name='应入住人数'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='age',
            field=models.IntegerField(verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='create_time',
            field=models.DateField(verbose_name='入寝时间'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='name',
            field=models.CharField(max_length=16, verbose_name='寝室人员姓名'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=64, verbose_name='  密码'),
        ),
        migrations.CreateModel(
            name='ArticalPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_updated', models.SmallIntegerField(choices=[(1, '原始留言'), (2, '已编辑')], default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.userinfo')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
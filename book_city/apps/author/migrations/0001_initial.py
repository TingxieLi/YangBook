# Generated by Django 2.0 on 2019-03-02 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=20, verbose_name='作者姓名')),
                ('desc', models.CharField(max_length=200, verbose_name='作者介绍')),
                ('attention_num', models.IntegerField(default=0, verbose_name='关注数')),
            ],
            options={
                'verbose_name': '作者信息',
                'verbose_name_plural': '作者信息',
            },
        ),
    ]
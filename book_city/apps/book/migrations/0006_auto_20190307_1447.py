# Generated by Django 2.0 on 2019-03-07 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20190307_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='sort_number',
            field=models.IntegerField(max_length=20, verbose_name='章节序号'),
        ),
    ]

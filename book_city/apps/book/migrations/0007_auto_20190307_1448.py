# Generated by Django 2.0 on 2019-03-07 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_auto_20190307_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='sort_number',
            field=models.IntegerField(verbose_name='章节序号'),
        ),
    ]

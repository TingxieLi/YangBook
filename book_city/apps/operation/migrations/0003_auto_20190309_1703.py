# Generated by Django 2.0 on 2019-03-09 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20190302_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='history_man',
        ),
        migrations.DeleteModel(
            name='History',
        ),
    ]

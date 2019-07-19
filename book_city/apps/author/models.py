from django.db import models
from db.base_model import BaseModel


class Author(BaseModel):
    name = models.CharField(max_length=20, unique=True, verbose_name='作者姓名')
    desc = models.CharField(max_length=200, verbose_name='作者介绍')
    avatar = models.ImageField(upload_to='author/', default='author/avatar.jpg', verbose_name='头像')
    attention_num = models.IntegerField(default=0, verbose_name='关注数')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '作者信息'
        verbose_name_plural = verbose_name

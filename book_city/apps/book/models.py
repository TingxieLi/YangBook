from django.db import models
from db.base_model import BaseModel
from author.models import Author


class Book(BaseModel):
    type_tuple = (
        ('wx', '武侠小说'),
        ('xh', '玄幻小说'),
        ('ds', '都市言情'),
        ('kb', '恐怖灵异'),
        ('xd', '现代文学'),
        ('zt', '侦探推理'),
        ('kh', '科幻小说'),
        ('cy', '穿越架空'),
        ('gd', '古典名著'),
        ('ls', '历史军事'),
        ('wy', '网游小说'),
    )
    image = models.ImageField(upload_to='book/', max_length=200, verbose_name='小说封面')
    title = models.CharField(max_length=100, unique=True, verbose_name='小说名称')
    type = models.CharField(choices=type_tuple, max_length=20, verbose_name='小说分类')
    status = models.SmallIntegerField(choices=((0, '已完结'), (1, '连载中')), default=1, verbose_name='状态')
    collect_num = models.IntegerField(default=0, verbose_name='收藏数')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    comment_num = models.IntegerField(default=0, verbose_name='评论数')
    recommend_num = models.IntegerField(default=0, verbose_name='推荐数')
    desc = models.TextField(verbose_name='小说介绍')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='作者')
    download_url = models.URLField(verbose_name='下载连接')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('create_time',)
        verbose_name = '书籍信息'
        verbose_name_plural = verbose_name


class Chapter(BaseModel):
    sort_number = models.IntegerField(verbose_name='章节序号')
    title = models.CharField(max_length=100, verbose_name='章节名称')
    content = models.TextField(verbose_name='章节内容')
    book = models.ForeignKey(Book, verbose_name='所属小说', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('sort_number',)
        verbose_name = '章节信息'
        verbose_name_plural = verbose_name


class Banner(BaseModel):
    book = models.OneToOneField(Book, max_length=200, verbose_name='轮播图关联书', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name='图片')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

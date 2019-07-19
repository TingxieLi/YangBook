from django.db import models
from db.base_model import BaseModel
from user.models import UserInfo
from book.models import Book, Chapter
from author.models import Author


class Collect(BaseModel):
    collect_man = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='收藏人')
    collect_book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='收藏书')

    def __str__(self):
        return self.collect_man.username

    class Meta:
        verbose_name = '收藏信息'
        verbose_name_plural = verbose_name


class Attention(BaseModel):
    attention_man = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='关注人')
    attention_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='关注作者')

    def __str__(self):
        return self.attention_man.username

    class Meta:
        verbose_name = '关注信息'
        verbose_name_plural = verbose_name


class Comment(BaseModel):
    comment_man = models.ForeignKey(UserInfo, verbose_name='评论用户', on_delete=models.CASCADE)
    comment_book = models.ForeignKey(Book, verbose_name='评论书本', on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=300, verbose_name='评论内容')

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ('-create_time',)
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name


class Recommend(BaseModel):
    recommend_man = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='推荐人')
    recommend_book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='推荐书')
    recommend_num = models.IntegerField(default=1, verbose_name='推荐数')

    def __str__(self):
        return self.recommend_man.username

    class Meta:
        ordering = ('-recommend_num',)
        verbose_name = '推荐信息'
        verbose_name_plural = verbose_name


class BookmarkModel(BaseModel):
    mark_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='书签用户')
    mark_book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='标记书籍')
    mark_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='书签章节')

    def __str__(self):
        return self.mark_user.username

    class Meta:
        unique_together = (('mark_user', 'mark_book'),)
        verbose_name = '书签信息'
        verbose_name_plural = verbose_name

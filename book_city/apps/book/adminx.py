import xadmin
from .models import Book, Chapter, Banner


class BookXadmin(object):
    list_display = ['image', 'title', 'type', 'status', 'collect_num', 'click_num', 'comment_num', 'recommend_num', 'author', 'download_url', 'create_time', 'update_time']
    search_fields = ['title']
    model_icon = 'fa fa-book'


class ChapterXadmin(object):
    list_display = ['sort_number', 'title', 'book', 'create_time', 'update_time']
    search_fields = ['title']
    model_icon = 'fa fa-file-text-o'


class BannerXadmin(object):
    list_display = ['book', 'image', 'create_time', 'update_time']
    model_icon = 'fa fa-file-image-o'


xadmin.site.register(Book, BookXadmin)
xadmin.site.register(Chapter, ChapterXadmin)
xadmin.site.register(Banner, BannerXadmin)

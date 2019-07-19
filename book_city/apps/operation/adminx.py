import xadmin
from .models import Collect, Attention, Comment, BookmarkModel


class CollectXadmin(object):
    list_display = ['collect_man', 'collect_book', 'create_time', 'update_time']
    search_fields = ['collect_man']
    model_icon = 'fa fa-heart'


class AttentionXadmin(object):
    list_display = ['attention_man', 'attention_author', 'create_time', 'update_time']
    search_fields = ['attention_man']
    model_icon = 'fa fa-heartbeat'


class CommentXadmin(object):
    list_display = ['comment_man', 'comment_book', 'comment_content', 'create_time', 'update_time']
    search_fields = ['comment_man']
    model_icon = 'fa fa-comment'


class BookmarkModelXadmin(object):
    list_display = ['mark_user', 'mark_book', 'mark_chapter', 'create_time', 'update_time']
    search_fields = ['mark_user']
    model_icon = 'fa fa-bookmark'


xadmin.site.register(Collect, CollectXadmin)
xadmin.site.register(Attention, AttentionXadmin)
xadmin.site.register(Comment, CommentXadmin)
xadmin.site.register(BookmarkModel, BookmarkModelXadmin)

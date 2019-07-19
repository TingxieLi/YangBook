import xadmin
from .models import Author


class AuthorXadmin(object):
    list_display = ['name', 'desc', 'attention_num', 'create_time', 'update_time']
    search_fields = ['name']
    model_icon = 'fa fa-mortar-board'


xadmin.site.register(Author, AuthorXadmin)

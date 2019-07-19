import xadmin
from .models import Member
from xadmin import views


class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True


class CommonXadminSetting(object):
    site_title = '阳哥书城后台'
    site_footer = '阳哥书城'
    menu_style = 'accordion'


class MemberXadmin(object):
    list_display = ['member_user', 'ticket_num', 'deadline', 'create_time', 'update_time']
    search_fields = ['member_user']
    model_icon = 'fa fa-star'


xadmin.site.register(views.BaseAdminView, BaseXadminSetting)
xadmin.site.register(views.CommAdminView, CommonXadminSetting)

xadmin.site.register(Member, MemberXadmin)


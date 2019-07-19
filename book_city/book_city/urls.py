import xadmin
from django.urls import path, include
from book.views import IndexView

urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('author/', include('author.urls')),
    path('book/', include('book.urls')),
    path('operation/', include('operation.urls')),
    path('trade/', include('trade.urls')),
    path('user/', include('user.urls')),
    path('', IndexView.as_view(), name='index')
]

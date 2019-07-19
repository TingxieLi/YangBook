from django.urls import path
from .views import OrderView, PayView

app_name = 'trade'
urlpatterns = [
    path('order', OrderView.as_view(), name='order'),
    path('pay', PayView.as_view(), name='pay'),
]

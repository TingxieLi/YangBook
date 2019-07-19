from django.urls import path
from .views import AuthorDetailView

app_name = 'author'
urlpatterns = [
    path('<int:author_id>', AuthorDetailView.as_view(), name='detail')
]

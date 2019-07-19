from django.urls import path
from .views import TypeView, RankView, DetailView, ChapterView, ContentView

app_name = 'book'
urlpatterns = [
    path('type/<slug:category>/<int:page_num>', TypeView.as_view(), name='type'),
    path('rank/<slug:sort>/<int:page_num>', RankView.as_view(), name='rank'),
    path('book/<int:book_id>', DetailView.as_view(), name='detail'),
    path('chapter/<int:book_id>', ChapterView.as_view(), name='chapter'),
    path('content/<int:chapter_id>', ContentView.as_view(), name='content')
]

from django.urls import path
from .views import SearchView, CollectView, AttentionView, DeleteHistoryView, CommentView, RecommendView, BookmarkView, DownloadView


app_name = 'operation'
urlpatterns = [
    path('search', SearchView.as_view(), name='search'),
    path('collect', CollectView.as_view(), name='collect'),
    path('recommend', RecommendView.as_view(), name='recommend'),
    path('attention', AttentionView.as_view(), name='attention'),
    path('delete_history', DeleteHistoryView.as_view(), name='delete_history'),
    path('comment', CommentView.as_view(), name='comment'),
    path('bookmark', BookmarkView.as_view(), name='bookmark'),
    path('download', DownloadView.as_view(), name='download'),
]
